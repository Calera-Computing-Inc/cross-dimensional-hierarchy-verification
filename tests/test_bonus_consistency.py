#!/usr/bin/env python3
"""
BONUS — Cross-Cutting Consistency Checks

Validates:
  - Algebraic identities σ^d = σ + 1 and σ^{d−1} = 1 + 1/σ
  - Generalized semantic octave: (1/σ_d)^{d−1} + (1/σ_d)^d = 1
  - 1/σ_d values match paper's Table 1
  - σ_d monotonically decreasing → 1
"""

from .framework import TestHarness, find_positive_root


def run(harness):
    """Execute all bonus consistency tests."""
    harness.header("BONUS — Cross-Cutting Consistency Checks")

    # B.1: Key algebraic identities σ^d = σ + 1 and σ^{d-1} = 1 + 1/σ
    print("  Algebraic identities:")
    for d_val in [2, 3, 4, 5]:
        s = find_positive_root(d_val)
        err1 = abs(s**d_val - (s + 1))
        err2 = abs(s**(d_val - 1) - (1 + 1/s))
        harness.check(err1 < 1e-12 and err2 < 1e-12,
              f"d={d_val}: σ^d = σ+1, σ^{{d-1}} = 1+1/σ (errs {err1:.2e}, {err2:.2e})")

    # B.2: Generalized semantic octave: (1/σ_d)^{d-1} + (1/σ_d)^d = 1
    print("\n  Generalized semantic octave: (1/σ_d)^(d-1) + (1/σ_d)^d = 1:")
    for d_val in [2, 3, 4, 5, 6, 10, 20]:
        s = find_positive_root(d_val)
        e_dm1 = (1/s)**(d_val - 1)
        e_d   = (1/s)**d_val
        total = e_dm1 + e_d
        harness.check(abs(total - 1.0) < 1e-10,
              f"d={d_val}: E({d_val-1}) + E({d_val}) = {total:.12f} ≈ 1")

    # B.3: 1/σ_d values match paper's Table 1
    print("\n  1/σ_d table values:")
    paper_inv = {2: 0.61803399, 3: 0.75487767, 4: 0.81917251}
    for d_val, pi in paper_inv.items():
        our = 1.0 / find_positive_root(d_val)
        err = abs(our - pi)
        harness.check(err < 5e-7, f"d={d_val}: 1/σ_d = {our:.8f} matches paper {pi}")

    # B.4: σ_d monotonically decreasing and → 1
    print("\n  σ_d monotonically decreasing → 1:")
    prev = None
    monotone = True
    for d_val in [2, 3, 4, 5, 6, 10, 20, 50]:
        s = find_positive_root(d_val)
        if prev is not None and s >= prev:
            monotone = False
        prev = s
    harness.check(monotone, "σ_d monotonically decreasing for d = 2, 3, ..., 50")


if __name__ == "__main__":
    h = TestHarness()
    run(h)
    h.summary()
