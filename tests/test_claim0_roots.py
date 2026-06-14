#!/usr/bin/env python3
"""
Claim 0 — Polynomial Roots σ_d: x^d = x + 1

Validates:
  - Known constants φ, ρ, σ match Newton solver output
  - Residuals |x^d − x − 1| < 2×10⁻¹⁵ for d = 2..10
  - Paper's Table 1 truncated values
"""

from .framework import PHI, RHO, SIGMA, TestHarness, find_positive_root


def run(harness):
    """Execute all Claim 0 tests."""
    harness.header("Claim 0 — Polynomial Roots σ_d: x^d = x + 1")

    # 0.1: Known constants match
    for d_val, name, ref in [(2, 'φ (golden ratio)', PHI),
                              (3, 'ρ (plastic constant)', RHO),
                              (4, 'σ (sigma-constant)', SIGMA)]:
        s = find_positive_root(d_val)
        err = abs(s - ref)
        residual = abs(s**d_val - s - 1)
        print(f"  σ_{d_val} = {s:.15f}  ({name})")
        print(f"       reference = {ref:.15f}, error = {err:.2e}")
        harness.check(err < 1e-12, f"σ_{d_val} = {name}, error {err:.2e} < 1e-12")
        harness.check(residual < 2e-15, f"|σ_{d_val}^{d_val} − σ_{d_val} − 1| = {residual:.2e} < 2e-15")

    # 0.2: All roots d=2..10 satisfy the polynomial to machine precision
    for d_val in range(2, 11):
        s = find_positive_root(d_val)
        residual = abs(s**d_val - s - 1)
        harness.check(residual < 2e-15, f"d={d_val}: |x^d − x − 1| = {residual:.2e} < 2e-15")

    # 0.3: Paper's Table 1 truncated values
    paper_table1 = {2: 1.61803399, 3: 1.32471796, 4: 1.22074408}
    for d_val, pv in paper_table1.items():
        s = find_positive_root(d_val)
        err = abs(s - pv)
        harness.check(err < 5e-7, f"Table 1: σ_{d_val} = {s:.8f} matches {pv} (err {err:.2e})")


if __name__ == "__main__":
    h = TestHarness()
    run(h)
    h.summary()
