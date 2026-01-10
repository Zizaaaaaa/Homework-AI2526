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

    time_s: float
    expanded: int
    generated: int

    bf_min: int
    bf_max: int
    bf_avg: float

    max_frontier: int
    max_closed: int
    max_memory: int

@dataclass
class AStarLimits:
    time_limit_s: Optional[float] = None
    max_memory_states: Optional[int] = None

def astar(n: int,
    start: Tuple[int, ...],
    goal: Optional[Tuple[int, ...]] = None,
    limits: Optional[AStarLimits] = None,
) -> AStarResult:
    if goal is None:
        goal = goal_state(n)
    if limits is None:
        limits = AStarLimits()

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
    max_closed = 0
    max_memory = 1

    bf_sum = 0
    bf_min = 10**9
    bf_max = 0

    while heap:
        # timeout
        if limits.time_limit_s is not None:
            if (time.perf_counter() - t0) > limits.time_limit_s:
                break
        max_frontier = max(max_frontier, len(heap))
        max_closed = max(max_closed, len(closed))
        max_memory = max(max_memory, len(heap) + len(closed))

        if limits.max_memory_states is not None and max_memory > limits.max_memory_states:
            break

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

            elapsed = time.perf_counter() - t0
            bf_avg = (bf_sum / expanded) if expanded > 0 else 0.0
            if bf_min == 10**9:
                bf_min = 0

            return AStarResult(
                solved=True,
                plan=plan,
                cost=len(plan),
                time_s=elapsed,
                expanded=expanded,
                generated=generated,
                bf_min=bf_min,
                bf_max=bf_max,
                bf_avg=bf_avg,
                max_frontier=max_frontier,
                max_closed=max_closed,
                max_memory=max_memory,
            )

        expanded += 1

        deg = 0
        for mv, s2 in neighbors(n, state):
            deg += 1
            if s2 in closed:
                continue

            # Duplicate elimination on OPEN:
            # keep only the best g seen so far for a state (but do not reopen closed ones).
            tentative_g = g + 1
            old_g = g_score.get(s2)
            if old_g is None or tentative_g < old_g:
                g_score[s2] = tentative_g
                parent[s2] = (state, mv)
                h = manhattan(n, s2, goal)
                tie += 1
                heapq.heappush(heap, (tentative_g + h, tie, tentative_g, s2))
                generated += 1
        bf_sum += deg
        bf_min = min(bf_min, deg)
        bf_max = max(bf_max, deg)

    elapsed = time.perf_counter() - t0
    bf_avg = (bf_sum / expanded) if expanded > 0 else 0.0
    if bf_min == 10**9:
        bf_min = 0

    return AStarResult(
        solved=False,
        plan=[],
        cost=0,
        time_s=elapsed,
        expanded=expanded,
        generated=generated,
        bf_min=bf_min,
        bf_max=bf_max,
        bf_avg=bf_avg,
        max_frontier=max_frontier,
        max_closed=max_closed,
        max_memory=max_memory,
    )
