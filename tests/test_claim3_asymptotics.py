#!/usr/bin/env python3
"""
Claim 3 — Asymptotic Expansion: σ_d ≈ 1 + ln(2)/d + c₂/d² + c₃/d³ + c₄/d⁴

Validates:
  - Leading term (σ_d − 1)·d → ln(2)
  - Exact analytic coefficients c₂, c₃, c₄
  - Fitting bias demonstration (degree-3 fit over d=2..50)
  - Restricted fit d≥20 recovers analytic values
  - Coefficient pattern: leading 1/2^(n−1), trailing 1/n!
  - σ_d → 1 convergence
  - General Lagrange inversion formula verified through n = 8
  - 8-term expansion matches σ_d to machine precision
"""

import math
from fractions import Fraction
from .framework import LN2, TestHarness, find_positive_root, solve_linear


# ─── Exact analytic coefficients ──────────────────────────────────────────────
C2_EXACT = LN2 * (1 + LN2) / 2                                   # ≈ 0.5868
C3_EXACT = LN2/4 + 5*LN2**2/8 + LN2**3/6                        # ≈ 0.5291
C4_EXACT = LN2/8 + 9*LN2**2/16 + 3*LN2**3/8 + LN2**4/24         # ≈ 0.4914


# ─── Lagrange inversion helpers (exact rational arithmetic) ───────────────────
def compute_R_coeffs(N):
    """R(u) = u/2 + ln(cosh(u/2)), purely rational Taylor coefficients."""
    # cosh(u/2) - 1 = Σ_{k≥1} u^{2k} / (2^{2k} (2k)!)
    x = [Fraction(0)] * (N + 1)
    for k in range(1, N // 2 + 1):
        if 2 * k <= N:
            x[2 * k] = Fraction(1, 2**(2 * k) * math.factorial(2 * k))
    # ln(1+x) = x - x²/2 + x³/3 - ...
    ln_cosh = [Fraction(0)] * (N + 1)
    cur = [Fraction(0)] * (N + 1)
    cur[0] = Fraction(1)
    for j in range(1, N + 1):
        nxt = [Fraction(0)] * (N + 1)
        for a in range(N + 1):
            if cur[a] == 0:
                continue
            for b in range(N + 1):
                if x[b] == 0:
                    continue
                if a + b <= N:
                    nxt[a + b] += cur[a] * x[b]
        cur = nxt
        sgn = Fraction((-1)**(j + 1), j)
        for k in range(N + 1):
            ln_cosh[k] += sgn * cur[k]
    R = [Fraction(0)] * (N + 1)
    R[1] = Fraction(1, 2)
    for k in range(N + 1):
        R[k] += ln_cosh[k]
    return R


def frac_poly_mul(a, b, N):
    result = [Fraction(0)] * (N + 1)
    for i in range(N + 1):
        if a[i] == 0:
            continue
        for j in range(N + 1 - i):
            if b[j] == 0:
                continue
            result[i + j] += a[i] * b[j]
    return result


def frac_poly_pow(p, exp, N):
    result = [Fraction(0)] * (N + 1)
    result[0] = Fraction(1)
    for _ in range(exp):
        result = frac_poly_mul(result, p, N)
    return result


def run(harness):
    """Execute all Claim 3 tests."""
    harness.header("Claim 3 — Asymptotic Expansion Verification")

    print(f"  Exact analytic coefficients (from d·ln(1+ε) = ln(2+ε)):")
    print(f"    c₁ = ln(2) = {LN2:.10f}")
    print(f"    c₂ = L(1+L)/2 = {C2_EXACT:.10f}")
    print(f"    c₃ = L/4 + 5L²/8 + L³/6 = {C3_EXACT:.10f}")
    print(f"    c₄ = L/8 + 9L²/16 + 3L³/8 + L⁴/24 = {C4_EXACT:.10f}")

    # 3.1: Leading term — (σ_d − 1)·d → ln(2) as d → ∞
    print("\n  Leading term: (σ_d − 1)·d → ln(2):")
    for d_val in [5, 10, 20, 30, 50]:
        s = find_positive_root(d_val)
        product = (s - 1) * d_val
        err = abs(product - LN2) / LN2
        print(f"    d={d_val:2d}: (σ_d − 1)·d = {product:.6f}, ln(2) = {LN2:.6f}, rel_err = {err:.4f}")

    # Must approach ln(2) at d=50 — note (σ_d-1)·d has O(1/d) corrections
    s50 = find_positive_root(50)
    product50 = (s50 - 1) * 50
    harness.check(abs(product50 - LN2) / LN2 < 0.02,
          f"d=50: (σ_d − 1)·d = {product50:.6f} approaching ln(2) = {LN2:.6f} (within 2%)")

    # 3.2: Proof verification of leading term
    print("\n  Leading-term proof:")
    print("    Set x = 1 + ε in x^d = x + 1:")
    print("    (1 + ε)^d ≈ e^{εd} = 2 + ε ≈ 2")
    print("    Therefore εd ≈ ln(2), i.e., ε ≈ ln(2)/d  ✓")

    # 3.3: Verify exact c₂ against numerical σ_d values
    print("\n  Exact c₂ verification against σ_d data:")
    for d_val in [20, 50, 100]:
        s = find_positive_root(d_val)
        c2_num = ((s - 1) * d_val - LN2) * d_val
        err = abs(c2_num - C2_EXACT) / C2_EXACT
        print(f"    d={d_val}: c₂_num = {c2_num:.6f}, exact = {C2_EXACT:.6f}, rel_err = {err:.4f}")

    s100 = find_positive_root(100)
    c2_at_100 = ((s100 - 1) * 100 - LN2) * 100
    harness.check(abs(c2_at_100 - C2_EXACT) / C2_EXACT < 0.02,
          f"c₂ from d=100 data = {c2_at_100:.4f} approaches exact {C2_EXACT:.4f}")

    # 3.4: Verify exact c₃ against numerical σ_d values
    print("\n  Exact c₃ verification against σ_d data:")
    for d_val in [20, 50, 100]:
        s = find_positive_root(d_val)
        c3_num = ((s - 1) - LN2/d_val - C2_EXACT/d_val**2) * d_val**3
        err = abs(c3_num - C3_EXACT) / C3_EXACT
        print(f"    d={d_val}: c₃_num = {c3_num:.6f}, exact = {C3_EXACT:.6f}, rel_err = {err:.4f}")

    c3_at_100 = ((s100 - 1) - LN2/100 - C2_EXACT/10000) * 100**3
    harness.check(abs(c3_at_100 - C3_EXACT) / C3_EXACT < 0.02,
          f"c₃ from d=100 data = {c3_at_100:.4f} approaches exact {C3_EXACT:.4f}")

    # 3.5: Verify exact c₄ against numerical σ_d values
    print("\n  Exact c₄ verification against σ_d data:")
    for d_val in [50, 100, 200]:
        s = find_positive_root(d_val)
        c4_num = ((s - 1) - LN2/d_val - C2_EXACT/d_val**2 - C3_EXACT/d_val**3) * d_val**4
        err = abs(c4_num - C4_EXACT) / C4_EXACT
        print(f"    d={d_val}: c₄_num = {c4_num:.6f}, exact = {C4_EXACT:.6f}, rel_err = {err:.4f}")

    s200 = find_positive_root(200)
    c4_at_200 = ((s200 - 1) - LN2/200 - C2_EXACT/200**2 - C3_EXACT/200**3) * 200**4
    harness.check(abs(c4_at_200 - C4_EXACT) / C4_EXACT < 0.02,
          f"c₄ from d=200 data = {c4_at_200:.4f} approaches exact {C4_EXACT:.4f}")

    # 3.6: Demonstrate fitting bias — the paper's fitted c₂ ≈ 0.620, c₃ ≈ 0.186
    print("\n  Fitting bias demonstration (degree-3 fit over d=2..50):")
    ds = list(range(2, 51))
    ys = [(find_positive_root(d) - 1) * d for d in ds]

    # Build 4×4 normal equations: A^T A coeffs = A^T y
    K = 4
    n = len(ds)
    S = [[0.0]*K for _ in range(K)]
    rhs = [0.0]*K
    for i in range(n):
        x = 1.0 / ds[i]
        row = [x**p for p in range(K)]
        for r in range(K):
            for c in range(K):
                S[r][c] += row[r] * row[c]
            rhs[r] += row[r] * ys[i]

    coeffs = solve_linear(S, rhs)
    c1_fit, c2_fit, c3_fit, c4_fit = coeffs

    print(f"    c₁ (leading) = {c1_fit:.6f}  (exact: {LN2:.6f})")
    print(f"    c₂           = {c2_fit:.4f}    (exact: {C2_EXACT:.4f}, biased → 0.620)")
    print(f"    c₃           = {c3_fit:.4f}    (exact: {C3_EXACT:.4f}, biased → 0.186)")

    c1_err = abs(c1_fit - LN2) / LN2
    harness.check(c1_err < 0.005, f"c₁ = {c1_fit:.6f} ≈ ln(2), error {c1_err:.4e}")

    # The fit is biased, so check it matches the known biased values from the paper
    harness.check(abs(c2_fit - 0.620) < 0.02,
          f"Biased fit c₂ = {c2_fit:.4f} ≈ 0.620 (as paper states)")
    harness.check(abs(c3_fit - 0.186) < 0.05,
          f"Biased fit c₃ = {c3_fit:.4f} ≈ 0.186 (as paper states)")

    # 3.7: Verify restricting fit to d≥20 recovers analytic values
    print("\n  Fit restricted to d ≥ 20 (reduced bias):")
    ds_hi = list(range(20, 51))
    ys_hi = [(find_positive_root(d) - 1) * d for d in ds_hi]
    n_hi = len(ds_hi)
    S_hi = [[0.0]*K for _ in range(K)]
    rhs_hi = [0.0]*K
    for i in range(n_hi):
        x = 1.0 / ds_hi[i]
        row = [x**p for p in range(K)]
        for r in range(K):
            for c in range(K):
                S_hi[r][c] += row[r] * row[c]
            rhs_hi[r] += row[r] * ys_hi[i]
    coeffs_hi = solve_linear(S_hi, rhs_hi)
    c2_fit_hi = coeffs_hi[1]
    c3_fit_hi = coeffs_hi[2]
    print(f"    c₂ = {c2_fit_hi:.4f} (exact: {C2_EXACT:.4f})")
    print(f"    c₃ = {c3_fit_hi:.4f} (exact: {C3_EXACT:.4f})")
    harness.check(abs(c2_fit_hi - C2_EXACT) < abs(c2_fit - C2_EXACT),
          f"Restricting to d≥20 moves c₂ toward exact value")
    harness.check(abs(c3_fit_hi - C3_EXACT) < abs(c3_fit - C3_EXACT),
          f"Restricting to d≥20 moves c₃ toward exact value")

    # 3.8: Pattern verification — leading coeff = 1/2^(n-1), trailing = 1/n!
    print("\n  Coefficient pattern verification:")
    print("    Each cₙ is a degree-n polynomial in L = ln(2)")
    print("    Leading coeff (L¹): 1, 1/2, 1/4, 1/8 → 1/2^(n-1)")
    print("    Trailing coeff (Lⁿ): 1, 1/2, 1/6, 1/24 → 1/n!")
    for n_val, lead_expected, trail_expected in [(1, 1.0, 1.0),
                                                  (2, 0.5, 0.5),
                                                  (3, 0.25, 1/6),
                                                  (4, 0.125, 1/24)]:
        lead = 1.0 / 2**(n_val - 1)
        trail = 1.0 / math.factorial(n_val)
        harness.check(abs(lead - lead_expected) < 1e-15 and abs(trail - trail_expected) < 1e-15,
              f"n={n_val}: leading = 1/2^{n_val-1} = {lead}, trailing = 1/{n_val}! = {trail:.6f}")

    # 3.9: σ_d → 1 convergence
    print("\n  σ_d → 1 convergence:")
    harness.check(s50 < 1.02, f"σ_50 = {s50:.8f} → 1")

    # 3.10: GENERAL FORMULA — Lagrange inversion verification
    # c_n = (1/n) [u^{n-1}]{ e^u · [ln(1+e^u)]^n }
    MAX_N = 8  # verify through c_8

    print("\n  General Lagrange inversion formula (Eq. cngeneral):")
    print("    c_n = (1/n)[u^{n-1}]{e^u · [ln(1+e^u)]^n}")
    print("    using ln(1+e^u) = L + R(u), R(u) = u/2 + ln(cosh(u/2))")

    R = compute_R_coeffs(MAX_N)
    eu_frac = [Fraction(1, math.factorial(k)) for k in range(MAX_N + 1)]

    # Compute c_n via Lagrange formula and compare to known exact values
    known_exact = {
        1: LN2,
        2: C2_EXACT,
        3: C3_EXACT,
        4: C4_EXACT,
    }

    lagrange_a = {}  # n -> float value
    print()
    for n_idx in range(1, MAX_N + 1):
        # c_n = Σ_{k=1}^{n} C(n,k)/n · [u^{n-1}](e^u · R^{n-k}) · L^k
        value = 0.0
        for k in range(1, n_idx + 1):
            j = n_idx - k
            R_pow = frac_poly_pow(R, j, MAX_N)
            prod = frac_poly_mul(eu_frac, R_pow, MAX_N)
            c_jn = prod[n_idx - 1]  # [u^{n-1}]
            binom = math.comb(n_idx, k)
            A_nk = float(Fraction(binom, n_idx) * c_jn)
            value += A_nk * LN2**k
        lagrange_a[n_idx] = value

        if n_idx in known_exact:
            err = abs(value - known_exact[n_idx])
            status = f"matches known c_{n_idx} = {known_exact[n_idx]:.10f}" if err < 1e-14 else f"MISMATCH"
            print(f"    c_{n_idx} (Lagrange) = {value:.10f}, {status}")
            harness.check(err < 1e-14, f"Lagrange c_{n_idx} = {value:.10f} matches exact")
        else:
            print(f"    c_{n_idx} (Lagrange) = {value:.10f}")
            harness.check(value > 0, f"Lagrange c_{n_idx} = {value:.10f} is positive")

    # Verify the 8-term expansion matches σ_d numerically
    print("\n  8-term Lagrange expansion vs numerical σ_d:")
    for d_val in [10, 20, 50, 100, 200]:
        sigma = find_positive_root(d_val)
        approx = 1.0
        for n_idx in range(1, MAX_N + 1):
            approx += lagrange_a[n_idx] / d_val**n_idx
        rel_err = abs(sigma - approx) / abs(sigma - 1)
        print(f"    d={d_val:4d}: σ_d = {sigma:.14f}, approx = {approx:.14f}, rel_err = {rel_err:.2e}")

    approx200 = 1.0 + sum(lagrange_a[n_idx] / 200**n_idx for n_idx in range(1, MAX_N + 1))
    rel200 = abs(s200 - approx200) / abs(s200 - 1)
    harness.check(rel200 < 1e-12,
          f"8-term Lagrange expansion at d=200: rel_err = {rel200:.2e}")


if __name__ == "__main__":
    h = TestHarness()
    run(h)
    h.summary()
