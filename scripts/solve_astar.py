from __future__ import annotations
import argparse

from npuzzle.puzzle import parse_state, scramble
from npuzzle.astar import astar


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--state", type=str, help='e.g. "1,2,3,4,5,6,7,0,8"')
    ap.add_argument("--scramble", type=int, help="scramble length k (from goal)")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    if args.state:
        start = parse_state(args.state)
    else:
        if args.scramble is None:
            raise SystemExit("Provide --state or --scramble")
        start = scramble(args.n, args.scramble, args.seed)

    res = astar(args.n, start)

    print(f"solved={res.solved}")
    print(f"time_s={res.time_s:.4f}")
    print(f"plan_len={len(res.plan)}")
    print(f"expanded={res.expanded} generated={res.generated} max_frontier={res.max_frontier}")
    if res.solved:
        print("plan:", " ".join(res.plan))


if __name__ == "__main__":
    main()
