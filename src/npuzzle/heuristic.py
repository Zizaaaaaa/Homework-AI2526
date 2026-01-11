from __future__ import annotations
from typing import Tuple


def manhattan(n: int, state: Tuple[int, ...], goal: Tuple[int, ...] | None = None) -> int:
    # goal default: 1..n*n-1,0
    # precompute the target position of every tile
    if goal is None:
        # goal standard
        goal_pos = {v: i for i, v in enumerate(list(range(1, n * n)) + [0])}
    else:
        goal_pos = {v: i for i, v in enumerate(goal)}

    dist = 0
    for i, v in enumerate(state):
        if v == 0:
            continue
        gi = goal_pos[v]
        r1, c1 = divmod(i, n)
        r2, c2 = divmod(gi, n)
        dist += abs(r1 - r2) + abs(c1 - c2)
    return dist
