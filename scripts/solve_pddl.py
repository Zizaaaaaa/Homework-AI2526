from __future__ import annotations

import argparse
from pathlib import Path

from npuzzle.pddl_runner import run_fast_downward_via_wsl
from problem_writer import generate_problem_pddl, parse_state  # usa le funzioni del file


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--state", type=str, required=True)
    ap.add_argument("--domain", type=str, default="pddl/domain.pddl")
    ap.add_argument("--problem", type=str, default="pddl/problem.pddl")
    args = ap.parse_args()

    state = parse_state(args.state)

    problem_text = generate_problem_pddl(
        n=args.n,
        state=state,
        problem_name="npuzzle",
        domain_name="npuzzle_domain",
    )

    problem_path = Path(args.problem)
    problem_path.parent.mkdir(parents=True, exist_ok=True)
    problem_path.write_text(problem_text, encoding="utf-8")
    print(f"Wrote: {problem_path}")

    actions = run_fast_downward_via_wsl(
        domain_path_win=Path(args.domain),
        problem_path_win=problem_path,
        search='astar(lmcut())',
        timeout_s=60,
    )

    print("\nPlan:")
    for i, a in enumerate(actions, 1):
        print(f"{i}. slide {a.tile} {a.src} -> {a.dst} (cost={a.cost})")


if __name__ == "__main__":
    main()
