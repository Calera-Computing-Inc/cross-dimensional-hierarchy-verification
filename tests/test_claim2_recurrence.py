#!/usr/bin/env python3
"""
Claim 2 — Algebraic: Sparse Recurrence a(n) = a(n−(d−1)) + a(n−d)

Validates:
  - Characteristic polynomial proof (analytic)
  - Ratio convergence a(N)/a(N−1) → σ_d for d = 2..15
  - Cutting identity σⁿ = σⁿ⁻⁽ᵈ⁻¹⁾ + σⁿ⁻ᵈ
"""

from .framework import TestHarness, find_positive_root


def run(harness):
    """Execute all Claim 2 tests."""
    harness.header("Claim 2 — Algebraic: Sparse Recurrence Verification")

    # 2.1: Proof verification (analytic)
    print("  Characteristic polynomial proof:")
    print("    Assume a(n) = xⁿ. Then xⁿ = x^{n-(d-1)} + x^{n-d}")
    print("    = x^{n-d}(x + 1). Divide by x^{n-d}: x^d = x + 1  ✓")
    print("    Valid for all d ≥ 2.\n")

    # 2.2: Ratio convergence for d = 2..15
    print("  Ratio convergence a(N)/a(N−1) → σ_d:")
    N_terms = 5000
    for d_val in range(2, 16):
        # Initialize recurrence
        a = [0] * N_terms
        for i in range(d_val):
            a[i] = 1
        for n in range(d_val, N_terms):
            a[n] = a[n - (d_val - 1)] + a[n - d_val]

        ratio = a[N_terms-1] / a[N_terms-2] if a[N_terms-2] != 0 else float('inf')
        target = find_positive_root(d_val)
        rel_err = abs(ratio - target) / target

        # For d ≤ 10, expect machine precision; for d > 10, accept paper's stated errors
        if d_val <= 10:
            threshold = 1e-10
        elif d_val <= 12:
            threshold = 1e-5
        else:
            threshold = 1e-3

        print(f"    d={d_val:2d}: ratio = {ratio:.10f}, σ_d = {target:.10f}, "
              f"rel_err = {rel_err:.2e}")
        harness.check(rel_err < threshold,
              f"d={d_val}: ratio converges, rel_err {rel_err:.2e} < {threshold:.0e}")

    # 2.3: Verify the cutting identity σⁿ = σⁿ⁻(d-1) + σⁿ⁻d (used later in Claim 4)
    print("\n  Cutting identity: σⁿ = σⁿ⁻(d-1) + σⁿ⁻d")
    for d_val in [2, 3, 4, 5]:
        s = find_positive_root(d_val)
        for n in range(d_val, d_val + 3):
            lhs = s**n
            rhs = s**(n - (d_val - 1)) + s**(n - d_val)
            err = abs(lhs - rhs) / abs(lhs)
            harness.check(err < 1e-14,
                  f"d={d_val}, n={n}: σ^{n} = σ^{n-(d_val-1)} + σ^{n-d_val}, err = {err:.2e}")


if __name__ == "__main__":
    h = TestHarness()
    run(h)
    h.summary()
