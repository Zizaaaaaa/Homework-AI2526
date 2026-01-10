from __future__ import annotations
import argparse
from typing import List, Optional

def pos_name(r: int, c: int) -> str:
    return f"p{r}_{c}"


def parse_state(s: str) -> List[int]:
    # accetta "1,2,3,4,5,6,7,0,8" oppure "1 2 3 4 5 6 7 0 8"
    s = s.replace(",", " ").strip()
    parts = [p for p in s.split() if p]
    return [int(x) for x in parts]


def default_goal(n: int) -> List[int]:
    return list(range(1, n * n)) + [0]


def generate_problem_pddl(
    n: int,
    state: List[int],
    goal: Optional[List[int]] = None,
    problem_name: str = "npuzzle_problem",
    domain_name: str = "npuzzle_domain",
) -> str:
    if len(state) != n * n:
        raise ValueError(f"State length {len(state)} != n*n ({n*n})")

    if goal is None:
        goal = default_goal(n)
    if len(goal) != n * n:
        raise ValueError(f"Goal length {len(goal)} != n*n ({n*n})")

    # objects
    pos_objs = [pos_name(r, c) for r in range(n) for c in range(n)]
    tile_objs = [f"t{k}" for k in range(1, n * n)]

    # adjacency (bidirezionale)
    adj_facts: List[str] = []
    for r in range(n):
        for c in range(n):
            p = pos_name(r, c)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                rr, cc = r + dr, c + dc
                if 0 <= rr < n and 0 <= cc < n:
                    q = pos_name(rr, cc)
                    adj_facts.append(f"(adj {p} {q})")

    # init facts: at/empty
    init_facts: List[str] = []
    for idx, v in enumerate(state):
        r, c = divmod(idx, n)
        p = pos_name(r, c)
        if v == 0:
            init_facts.append(f"(empty {p})")
        else:
            init_facts.append(f"(at t{v} {p})")

    # goal facts
    goal_facts: List[str] = []
    for idx, v in enumerate(goal):
        r, c = divmod(idx, n)
        p = pos_name(r, c)
        if v == 0:
            goal_facts.append(f"(empty {p})")
        else:
            goal_facts.append(f"(at t{v} {p})")

    pddl = f"""(define (problem {problem_name}-{n}x{n})
  (:domain {domain_name})

  (:objects
    {' '.join(tile_objs)} - tile
    {' '.join(pos_objs)} - pos
  )

  (:init
    {' '.join(adj_facts)}
    {' '.join(init_facts)}
  )

  (:goal (and
    {' '.join(goal_facts)}
  ))
)
"""
    return pddl