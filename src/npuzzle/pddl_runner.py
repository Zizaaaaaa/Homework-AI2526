from __future__ import annotations

import os
import re
import shlex
import time
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass(frozen=True)
class SlideAction:
    tile: str
    src: str
    dst: str
    cost: int = 1


def parse_sas_plan(plan_path: Path) -> List[SlideAction]:
    """
    Parse Fast Downward plan file (sas_plan). Expected lines like:
      slide t8 p2_2 p2_1 (1)
    Ignores empty lines and comments.
    """
    if not plan_path.exists():
        raise FileNotFoundError(f"Plan file not found: {plan_path}")

    actions: List[SlideAction] = []
    line_re = re.compile(
    r"^\s*\(?(?:slide)\s+(\S+)\s+(\S+)\s+(\S+)\)?(?:\s*\((\d+)\))?\s*$",
    re.IGNORECASE,) # accetta sia con parentesi sia senza

    for raw in plan_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith(";"):
            continue

        m = line_re.match(line)
        if not m:
            raise ValueError(f"Unrecognized plan line: {raw}")

        tile, src, dst, cost = m.group(1), m.group(2), m.group(3), m.group(4)
        actions.append(SlideAction(tile=tile, src=src, dst=dst, cost=int(cost) if cost else 1))

    return actions



def _windows_to_wsl_path(win_path: Path) -> str:
    win_str = str(win_path.resolve()).replace("\\", "/")  # Windows usa /, WSL usa \\
    proc = subprocess.run(                                # patterns delle dir incompatibili
        ["wsl", "wslpath", "-a", "-u", win_str],
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout.strip()



@dataclass
class FDResult:
    solved: bool
    plan: List[SlideAction]
    plan_len: int
    time_s: float  # total time (se trovato), altrimenti wall time stimata
    expanded: Optional[int]
    generated: Optional[int]


def _parse_fd_metrics(stdout: str) -> Tuple[Optional[int], Optional[int], Optional[int], Optional[float]]:
    # esempi:
    # "Expanded 2 state(s)."
    # "Generated 3 state(s)."
    # "Plan length: 1 step(s)."
    # "Total time: 0.010967s"
    exp = gen = plen = None
    total = None

    m = re.search(r"Expanded\s+(\d+)\s+state", stdout)
    if m:
        exp = int(m.group(1))
    m = re.search(r"Generated\s+(\d+)\s+state", stdout)
    if m:
        gen = int(m.group(1))
    m = re.search(r"Plan length:\s+(\d+)\s+step", stdout)
    if m:
        plen = int(m.group(1))
    m = re.search(r"Total time:\s+([0-9.]+)s", stdout)
    if m:
        total = float(m.group(1))

    return exp, gen, plen, total

def run_fast_downward_via_wsl(
    domain_path_win: Path,
    problem_path_win: Path,
    *,
    wsl_distro: str = "Ubuntu",
    fd_path_wsl: str = "$HOME/tools/downward/fast-downward.py",
    search: str = "astar(lmcut())",
    timeout_s: Optional[int] = None,
) -> FDResult:

    domain_path_win = domain_path_win.resolve()
    problem_path_win = problem_path_win.resolve()

    domain_wsl = _windows_to_wsl_path(domain_path_win)
    problem_wsl = _windows_to_wsl_path(problem_path_win)
    problem_dir_wsl = _windows_to_wsl_path(problem_path_win.parent)

    # cancella eventuali piani precedenti
    plan_dir = problem_path_win.parent
    for p in plan_dir.glob("sas_plan*"):
        try:
            p.unlink()
        except OSError:
            pass

    cmd = (
        f'cd {shlex.quote(problem_dir_wsl)} && '
        f'python3 "{fd_path_wsl}" '
        f'{shlex.quote(domain_wsl)} {shlex.quote(problem_wsl)} '
        f'--search {shlex.quote(search)} '
        f'--internal-plan-file sas_plan'
    )

    full = ["wsl", "-d", wsl_distro, "-e", "bash", "-lc", cmd]

    t0 = time.perf_counter()
    try:
        proc = subprocess.run(full, capture_output=True, text=True, timeout=timeout_s)
    except subprocess.TimeoutExpired:
        return FDResult(False, [], 0, float(timeout_s) if timeout_s else 0.0, None, None)

    wall_time = time.perf_counter() - t0

    out_all = (proc.stdout or "") + "\n" + (proc.stderr or "")

    # trova il piano più recente
    candidates = sorted(
        plan_dir.glob("sas_plan*"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    plan_file = next(
        (p for p in candidates if p.is_file() and p.stat().st_size > 0),
        None
    )

    plan = parse_sas_plan(plan_file) if plan_file else []
    solved = len(plan) > 0
    plan_len = len(plan)

    exp, gen, plen, total = _parse_fd_metrics(out_all)
    time_s = total if total is not None else wall_time

    return FDResult(solved, plan, plan_len, time_s, exp, gen)

