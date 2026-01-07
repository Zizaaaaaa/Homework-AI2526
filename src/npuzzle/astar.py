from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple
import heapq
import time

from .puzzle import Move, neighbors, goal_state
from .heuristic import manhattan


@dataclass
class AStarResult:
    solved: bool
    plan: List[Move]
    cost: int
    expanded: int
    generated: int
    max_frontier: int
    time_s: float


def astar(n: int, start: Tuple[int, ...], goal: Optional[Tuple[int, ...]] = None) -> AStarResult:
    if goal is None:
        goal = goal_state(n)

    t0 = time.perf_counter()

    # OPEN: priority queue (f, tie, g, state)
    heap: List[Tuple[int, int, int, Tuple[int, ...]]] = []
    tie = 0

    g_score: Dict[Tuple[int, ...], int] = {start: 0}
    parent: Dict[Tuple[int, ...], Tuple[Tuple[int, ...], Move]] = {}

    h0 = manhattan(n, start, goal)
    heapq.heappush(heap, (h0, tie, 0, start))

    closed: Set[Tuple[int, ...]] = set()

    expanded = 0
    generated = 1
    max_frontier = 1

    while heap:
        max_frontier = max(max_frontier, len(heap))
        _, _, g, state = heapq.heappop(heap)

        # If already closed, skip (stale entry).
        if state in closed:
            continue

        # Mark closed when we pop it for expansion => NO REOPENING.
        closed.add(state)

        if state == goal:
            plan: List[Move] = []
            cur = state
            while cur != start:
                prev, mv = parent[cur]
                plan.append(mv)
                cur = prev
            plan.reverse()
            return AStarResult(
                solved=True,
                plan=plan,
                cost=len(plan),
                expanded=expanded,
                generated=generated,
                max_frontier=max_frontier,
                time_s=time.perf_counter() - t0,
            )

        expanded += 1

        for mv, s2 in neighbors(n, state):
            if s2 in closed:
                continue  # NO REOPENING: ignore already-closed states

            tentative_g = g + 1

            # Duplicate elimination on OPEN:
            # keep only the best g seen so far for a state (but do not reopen closed ones).
            old_g = g_score.get(s2)
            if old_g is None or tentative_g < old_g:
                g_score[s2] = tentative_g
                parent[s2] = (state, mv)
                h = manhattan(n, s2, goal)
                tie += 1
                heapq.heappush(heap, (tentative_g + h, tie, tentative_g, s2))
                generated += 1

    return AStarResult(
        solved=False,
        plan=[],
        cost=0,
        expanded=expanded,
        generated=generated,
        max_frontier=max_frontier,
        time_s=time.perf_counter() - t0,
    )
