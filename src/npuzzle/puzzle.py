from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List, Tuple
from typing import List, Tuple
import random


Move = str  # "U","D","L","R"


def goal_state(n: int) -> Tuple[int, ...]:
    return tuple(list(range(1, n * n)) + [0])


def parse_state(s: str) -> Tuple[int, ...]:
    s = s.replace(",", " ").strip()
    parts = [p for p in s.split() if p]
    return tuple(int(x) for x in parts)


def find_zero(state: Tuple[int, ...]) -> int:
    return state.index(0)


def neighbors(n: int, state: Tuple[int, ...]) -> Iterable[Tuple[Move, Tuple[int, ...]]]:
    z = find_zero(state)
    r, c = divmod(z, n)

    def swap(i: int, j: int) -> Tuple[int, ...]:
        lst = list(state)
        lst[i], lst[j] = lst[j], lst[i]
        return tuple(lst)

    if r > 0:
        yield "U", swap(z, z - n)
    if r < n - 1:
        yield "D", swap(z, z + n)
    if c > 0:
        yield "L", swap(z, z - 1)
    if c < n - 1:
        yield "R", swap(z, z + 1)


def apply_move(n: int, state: Tuple[int, ...], move: Move) -> Tuple[int, ...]:
    # utile per verifiche
    for m, s2 in neighbors(n, state):
        if m == move:
            return s2
    raise ValueError(f"Illegal move {move} from state {state}")


def scramble(n: int, k: int, seed: int = 0) -> Tuple[int, ...]:
    rng = random.Random(seed)
    s = goal_state(n)
    last: Move | None = None
    # so as not to erase the previous move immediately (U <-> D, L <-> R)
    opp = {"U": "D", "D": "U", "L": "R", "R": "L"}
    for _ in range(k):
        options = [(m, s2) for (m, s2) in neighbors(n, s) if last is None or m != opp[last]]
        m, s = rng.choice(options)
        last = m
    return s


def random_walk(n: int, state: Tuple[int, ...], steps: int, seed: int | None = None) -> Tuple[int, ...]:
    """
    Generate a guaranteed-solvable n-puzzle state by applying `steps`
    random valid moves starting from `state` (usually the goal).
    """
    rng = random.Random(seed)
    current = state

    for _ in range(steps):
        zero = current.index(0)
        r, c = divmod(zero, n)

        moves = []
        if r > 0:
            moves.append(-n)      # up
        if r < n - 1:
            moves.append(n)       # down
        if c > 0:
            moves.append(-1)      # left
        if c < n - 1:
            moves.append(1)       # right

        delta = rng.choice(moves)
        nz = zero + delta

        lst = list(current)
        lst[zero], lst[nz] = lst[nz], lst[zero]
        current = tuple(lst)

    return current
