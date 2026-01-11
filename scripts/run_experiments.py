from __future__ import annotations
import argparse
import csv
from pathlib import Path

from npuzzle.puzzle import goal_state
from npuzzle.astar import astar, AStarLimits
from npuzzle.pddl_runner import run_fast_downward_via_wsl
from npuzzle.puzzle import random_walk


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="results/runs.csv")
    ap.add_argument("--seeds", type=int, default=20, help="number of seeds per (n,k)")
    ap.add_argument("--astar-timeout", type=float, default=10.0)
    ap.add_argument("--fd-timeout", type=int, default=30)
    ap.add_argument("--wsl-distro", type=str, default="Ubuntu")
    ap.add_argument("--domain", type=str, default="pddl/domain.pddl")
    ap.add_argument("--problem", type=str, default="pddl/problem.pddl")
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    domain_path = Path(args.domain)
    problem_path = Path(args.problem)

    # "sensible" experiment grid (a lot of run)
    # - Set A: sturdy curves su n=3 and n=4 (k bigger)
    # - Set B: n bigger but k smaller
    grid = []
    for k in [5, 10, 15, 20, 25, 30, 35, 40]:
        grid.append((3, k))
    for k in [5, 10, 15, 20, 25, 30]:
        grid.append((4, k))
    for n in [5, 6, 7, 8, 10]:
        for k in [5, 10, 15]:
            grid.append((n, k))

    fieldnames = [
        "n", "k", "seed", "method",
        "solved", "time_s", "plan_len",
        "expanded", "generated",
        "bf_min", "bf_max", "bf_avg",
        "max_frontier", "max_closed", "max_memory",
    ]

    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()

        for (n, k) in grid:
            for seed in range(args.seeds):
                start = goal_state(n)
                start = random_walk(n, start, k, seed=seed)

                # ----A*----
                ares = astar(
                    n, start, goal_state(n),
                    limits=AStarLimits(time_limit_s=args.astar_timeout, max_memory_states=None),
                )
                w.writerow({
                    "n": n, "k": k, "seed": seed, "method": "astar_manhattan",
                    "solved": ares.solved, "time_s": f"{ares.time_s:.6f}", "plan_len": len(ares.plan),
                    "expanded": ares.expanded, "generated": ares.generated,
                    "bf_min": ares.bf_min, "bf_max": ares.bf_max, "bf_avg": f"{ares.bf_avg:.6f}",
                    "max_frontier": ares.max_frontier, "max_closed": ares.max_closed, "max_memory": ares.max_memory,
                })

                # ----Planning (Fast Downward)----
                from npuzzle.pddl_problem import generate_problem_pddl

                problem_text = generate_problem_pddl(
                    n=n,
                    state=list(start),
                    problem_name="npuzzle",
                    domain_name="npuzzle_domain",
                )
                problem_path.write_text(problem_text, encoding="utf-8")

                fdres = run_fast_downward_via_wsl(
                    domain_path_win=domain_path,
                    problem_path_win=problem_path,
                    wsl_distro=args.wsl_distro,
                    timeout_s=args.fd_timeout,
                    search='astar(lmcut())',
                )

                w.writerow({
                    "n": n, "k": k, "seed": seed, "method": "fast_downward_lmcut",
                    "solved": fdres.solved, "time_s": f"{fdres.time_s:.6f}", "plan_len": fdres.plan_len,
                    "expanded": fdres.expanded if fdres.expanded is not None else "",
                    "generated": fdres.generated if fdres.generated is not None else "",
                    "bf_min": "", "bf_max": "", "bf_avg": "",
                    "max_frontier": "", "max_closed": "", "max_memory": "",
                })

    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
