#!/usr/bin/env python3
"""
Claim 4 — Van der Laan Hyperbox Subdivision: C(2d−1, d−1) types

Validates:
  - Self-similarity at first cut for d = 2..5
  - BFS exhaustive enumeration: 3, 10, 35, 126, 462 types for d = 2..6
  - Count matches C(2d−1, d−1) exactly
  - Volume conservation to machine precision
  - Combinatorial identity C(2d,d) − C(2d−1,d) = C(2d−1,d−1)
  - Ergodicity: cutting rule saturates the shape space
"""

import math
from collections import deque
from .framework import TestHarness, find_positive_root


# ─── Hyperbox helpers ─────────────────────────────────────────────────────────
def comb_val(n, r):
    """Binomial coefficient C(n,r) — pure Python."""
    if r < 0 or r > n:
        return 0
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))


def normalize_shape(shape):
    """Sort exponents and subtract the minimum so the smallest is 0."""
    s = sorted(shape)
    m = s[0]
    return tuple(x - m for x in s)


def cut_shape(shape, d):
    """
    Cut the longest side of a d-dimensional hyperbox.
    The cutting rule: σⁿ = σⁿ⁻⁽ᵈ⁻¹⁾ + σⁿ⁻ᵈ
    """
    shape_list = sorted(shape)
    max_exp = shape_list[-1]
    remaining = shape_list[:-1]

    piece1_new = max_exp - (d - 1)
    piece2_new = max_exp - d

    child1 = normalize_shape(tuple(remaining) + (piece1_new,))
    child2 = normalize_shape(tuple(remaining) + (piece2_new,))
    return child1, child2


def bfs_shapes(d):
    """BFS from the initial hyperbox to find all reachable proportional types."""
    initial = tuple(range(d))  # (0, 1, 2, ..., d-1)
    seen = {initial}
    queue = deque([initial])
    while queue:
        shape = queue.popleft()
        c1, c2 = cut_shape(shape, d)
        for child in [c1, c2]:
            if child not in seen:
                seen.add(child)
                queue.append(child)
    return seen


def run(harness):
    """Execute all Claim 4 tests."""
    harness.header("Claim 4 — Van der Laan Hyperbox Subdivision")

    # 4.1: Self-similarity at first cut — child₂ is clone of original
    print("  Self-similarity at first cut:")
    for d_val in [2, 3, 4, 5]:
        initial = tuple(range(d_val))
        c1, c2 = cut_shape(initial, d_val)
        is_clone = (c2 == initial)
        print(f"    d={d_val}: initial={initial}, child₁={c1}, child₂={c2}")
        harness.check(is_clone, f"d={d_val}: child₂ = {c2} is clone of original {initial}")

    # 4.2: BFS exhaustive enumeration — count matches C(2d−1, d−1)
    print("\n  BFS shape enumeration:")
    paper_counts = {2: 3, 3: 10, 4: 35, 5: 126, 6: 462}
    for d_val in range(2, 7):
        shapes = bfs_shapes(d_val)
        n_found = len(shapes)
        expected = comb_val(2 * d_val - 1, d_val - 1)
        paper_val = paper_counts[d_val]

        print(f"    d={d_val}: found {n_found} types, "
              f"C(2d−1,d−1) = {expected}, paper = {paper_val}")
        harness.check(n_found == expected, f"d={d_val}: BFS count {n_found} = C(2d−1,d−1) = {expected}")
        harness.check(n_found == paper_val, f"d={d_val}: matches paper count {paper_val}")

        # Max exponent spread should equal d
        max_spread = max(max(s) - min(s) for s in shapes)
        harness.check(max_spread == d_val, f"d={d_val}: max exponent spread = {max_spread} = d")

    # 4.3: Volume conservation at first cut
    print("\n  Volume conservation at first cut:")
    for d_val in [2, 3, 4, 5]:
        s = find_positive_root(d_val)
        # Original volume: σ^0 · σ^1 · ... · σ^{d-1} = σ^{sum(0..d-1)}
        original_exp_sum = d_val * (d_val - 1) // 2
        original_vol = s ** original_exp_sum

        max_exp = d_val - 1
        remaining_exps = list(range(d_val - 1))

        piece1_exp = max_exp - (d_val - 1)   # = 0
        piece2_exp = max_exp - d_val          # = -1

        child1_exps = remaining_exps + [piece1_exp]
        child2_exps = remaining_exps + [piece2_exp]

        vol1 = 1.0
        for e in child1_exps:
            vol1 *= s**e
        vol2 = 1.0
        for e in child2_exps:
            vol2 *= s**e

        err = abs(vol1 + vol2 - original_vol) / original_vol
        harness.check(err < 1e-14,
              f"d={d_val}: V₁ + V₂ = {vol1+vol2:.10f} ≈ V_orig = {original_vol:.10f}, err = {err:.2e}")

    # 4.4: Combinatorial identity C(2d,d) − C(2d−1,d) = C(2d−1,d−1)
    print("\n  Combinatorial identity C(2d,d) − C(2d−1,d) = C(2d−1,d−1):")
    for d_val in range(2, 7):
        lhs = comb_val(2*d_val, d_val) - comb_val(2*d_val - 1, d_val)
        rhs = comb_val(2*d_val - 1, d_val - 1)
        harness.check(lhs == rhs,
              f"d={d_val}: C({2*d_val},{d_val}) − C({2*d_val-1},{d_val}) = {lhs} = C({2*d_val-1},{d_val-1}) = {rhs}")

    # 4.5: Ergodicity check — all sorted d-tuples from {0,1,...,d} with min 0 are reachable
    print("\n  Ergodicity — all valid shapes reachable:")
    for d_val in range(2, 6):
        shapes = bfs_shapes(d_val)

        # Enumerate all sorted d-tuples from {0,...,d} with minimum 0
        def gen_tuples(dim, max_val):
            if dim == 1:
                return [(v,) for v in range(max_val + 1)]
            result = []
            for rest in gen_tuples(dim - 1, max_val):
                for v in range(rest[-1], max_val + 1):
                    result.append(rest + (v,))
            return result

        all_tuples = set()
        for t in gen_tuples(d_val, d_val):
            normed = normalize_shape(t)
            if min(normed) == 0:
                all_tuples.add(normed)

        missing = all_tuples - shapes
        extra = shapes - all_tuples
        harness.check(len(missing) == 0 and len(extra) == 0,
              f"d={d_val}: BFS shapes = all valid tuples ({len(shapes)} = {len(all_tuples)})")


if __name__ == "__main__":
    h = TestHarness()
    run(h)
    h.summary()
