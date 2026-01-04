from __future__ import annotations

import os
import re
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


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


from pathlib import Path
import subprocess

def _windows_to_wsl_path(win_path: Path) -> str:
    win_str = str(win_path.resolve()).replace("\\", "/")  # Windows usa /, WSL usa \\
    proc = subprocess.run(                                # patterns delle dir incompatibili
        ["wsl", "wslpath", "-a", "-u", win_str],
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout.strip()



def run_fast_downward_via_wsl(
    domain_path_win: Path,
    problem_path_win: Path,
    fd_path_wsl: str = "$HOME/tools/downward/fast-downward.py",
    search: str = 'astar(lmcut())',
    timeout_s: Optional[int] = None,
    keep_sas_plan_in_problem_dir: bool = True,
) -> List[SlideAction]:
    """
    Run Fast Downward through WSL from Windows Python.

    - domain_path_win/problem_path_win are Windows paths (Path objects).
    - fd_path_wsl is where fast-downward.py lives inside WSL.
    - Returns list of parsed SlideAction from sas_plan.
    """
    domain_path_win = domain_path_win.resolve()
    problem_path_win = problem_path_win.resolve()

    domain_wsl = _windows_to_wsl_path(domain_path_win)
    problem_wsl = _windows_to_wsl_path(problem_path_win)

    # run nella directory contenente il problema (sas_plan va lì)
    problem_dir_wsl = _windows_to_wsl_path(problem_path_win.parent)

    cmd = (
        f'cd {shlex.quote(problem_dir_wsl)} && '
        f'{fd_path_wsl} '
        f'{shlex.quote(domain_wsl)} {shlex.quote(problem_wsl)} '
        f'--search {shlex.quote(search)} '
    )
    if keep_sas_plan_in_problem_dir:
        cmd += f'--internal-plan-file sas_plan'

    full = ["wsl", "-d", "Ubuntu", "bash", "-lc", cmd]  # "Ubuntu" sennò chiama docker di default

    subprocess.run(full, check=True, timeout=timeout_s)

    plan_path = problem_path_win.parent / "sas_plan"
    return parse_sas_plan(plan_path)
