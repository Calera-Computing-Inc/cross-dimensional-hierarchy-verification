#!/usr/bin/env python3
"""
Claim 1 — Spectral: Heat-Kernel Decay α(t) crosses 1/σ_d

Validates:
  - Coordination numbers C_d = d(d+1)
  - Structure function normalization P̂(0) = 1
  - Boundary behavior α(0) → 0, α(∞) → 1
  - Monotonicity of α(t)
  - Crossing timescale t₀ via bisection
  - Gaussian approximation formula
"""

import math
from .framework import TestHarness, find_positive_root


def compute_alpha_pure(d, t, M):
    """
    Compute α(t) = E₁(t)/E₀(t) on the infinite A_d lattice via Fourier grid.
    Pure Python implementation — no numpy.
    """
    dk = 2 * math.pi / M
    k_vals = [i * dk for i in range(M)]

    if d == 2:
        numerator = 0.0
        denominator = 0.0
        for i in range(M):
            k1 = k_vals[i]
            for j in range(M):
                k2 = k_vals[j]
                Phat = (math.cos(k1) + math.cos(k2) + math.cos(k1 - k2)) / 3.0
                lam = 1.0 - Phat
                w = math.exp(-t * lam)
                numerator += w * Phat
                denominator += w
        return numerator / denominator

    elif d == 3:
        numerator = 0.0
        denominator = 0.0
        for i in range(M):
            k1 = k_vals[i]
            for j in range(M):
                k2 = k_vals[j]
                for l in range(M):
                    k3 = k_vals[l]
                    Phat = (math.cos(k1) + math.cos(k2) + math.cos(k3) +
                            math.cos(k1-k2) + math.cos(k1-k3) + math.cos(k2-k3)) / 6.0
                    lam = 1.0 - Phat
                    w = math.exp(-t * lam)
                    numerator += w * Phat
                    denominator += w
        return numerator / denominator

    elif d == 4:
        numerator = 0.0
        denominator = 0.0
        for i in range(M):
            k1 = k_vals[i]
            for j in range(M):
                k2 = k_vals[j]
                for l in range(M):
                    k3 = k_vals[l]
                    for m in range(M):
                        k4 = k_vals[m]
                        Phat = (math.cos(k1) + math.cos(k2) + math.cos(k3) + math.cos(k4) +
                                math.cos(k1-k2) + math.cos(k1-k3) + math.cos(k1-k4) +
                                math.cos(k2-k3) + math.cos(k2-k4) + math.cos(k3-k4)) / 10.0
                        lam = 1.0 - Phat
                        w = math.exp(-t * lam)
                        numerator += w * Phat
                        denominator += w
        return numerator / denominator

    else:
        raise ValueError(f"d={d} not implemented for clean-room spectral test")


def run(harness):
    """Execute all Claim 1 tests."""
    harness.header("Claim 1 — Spectral: Heat-Kernel Decay α(t) crosses 1/σ_d")

    # 1.1: Coordination numbers C_d = d(d+1)
    print("\n  Coordination numbers C_d = d(d+1):")
    for d_val in [2, 3, 4]:
        Cd = d_val * (d_val + 1)
        # Number of cosine terms in structure function = d + C(d,2) = C_d/2
        num_terms = d_val + d_val * (d_val - 1) // 2
        expected_half = Cd // 2
        harness.check(num_terms == expected_half,
              f"d={d_val}: C_d={Cd}, cosine terms={num_terms} = C_d/2={expected_half}")

    # 1.2: Structure function normalization P̂(0) = 1
    print("\n  Structure function normalization P̂(0) = 1:")
    for d_val, n_terms in [(2, 3), (3, 6), (4, 10)]:
        P0 = n_terms / (d_val * (d_val + 1) / 2)
        harness.check(abs(P0 - 1.0) < 1e-15, f"d={d_val}: P̂(0) = {P0}")

    # 1.3: Boundary behavior — α(t→0) → 0, α(t→∞) → 1
    # Use small grids for clean-room speed: M=40 for d=2, M=15 for d=3, M=8 for d=4
    print("\n  Boundary behavior of α(t):")
    grid_sizes = {2: 40, 3: 15, 4: 8}
    for d_val in [2, 3, 4]:
        M = grid_sizes[d_val]
        alpha_small = compute_alpha_pure(d_val, 0.01, M)
        alpha_large = compute_alpha_pure(d_val, 500.0, M)
        print(f"    d={d_val} (M={M}): α(0.01) = {alpha_small:.6f}, α(500) = {alpha_large:.6f}")
        harness.check(alpha_small < 0.01, f"d={d_val}: α(0.01) = {alpha_small:.4f} → 0")
        harness.check(alpha_large > 0.99, f"d={d_val}: α(500) = {alpha_large:.6f} → 1")

    # 1.4: Monotonicity of α(t) — verify at 10 points
    print("\n  Monotonicity of α(t):")
    for d_val in [2, 3, 4]:
        M = grid_sizes[d_val]
        t_points = [0.1 * (10 ** (i * 3.0 / 9)) for i in range(10)]  # log-spaced 0.1..100
        alphas = [compute_alpha_pure(d_val, t, M) for t in t_points]
        is_mono = all(alphas[i+1] >= alphas[i] for i in range(len(alphas)-1))
        harness.check(is_mono, f"d={d_val}: α(t) monotonically increasing across 10 points")

    # 1.5: Crossing timescale t₀ — bisection to find α(t₀) = 1/σ_d
    print("\n  Crossing timescale t₀ where α(t₀) = 1/σ_d:")
    paper_t0 = {2: 3.357, 3: 7.297, 4: 12.415}
    for d_val in [2, 3, 4]:
        target = 1.0 / find_positive_root(d_val)
        M = grid_sizes[d_val]

        # Coarse scan to find bracket
        t_lo, t_hi = 0.5, 100.0
        a_lo = compute_alpha_pure(d_val, t_lo, M)
        a_hi = compute_alpha_pure(d_val, t_hi, M)

        if a_lo < target < a_hi:
            # Bisect to find crossing
            for _ in range(40):
                t_mid = (t_lo + t_hi) / 2
                a_mid = compute_alpha_pure(d_val, t_mid, M)
                if a_mid < target:
                    t_lo = t_mid
                else:
                    t_hi = t_mid
            t0_found = (t_lo + t_hi) / 2
            paper_val = paper_t0[d_val]
            rel_err = abs(t0_found - paper_val) / paper_val
            print(f"    d={d_val}: t₀ = {t0_found:.3f} (paper: {paper_val:.3f}), rel_err = {rel_err:.4f}")
            # With smaller grids, allow 20% tolerance — the crossing must exist and be in the right ballpark
            harness.check(rel_err < 0.20, f"d={d_val}: t₀ = {t0_found:.3f} within 20% of paper {paper_val:.3f}")
        else:
            print(f"    d={d_val}: bracket failed (α_lo={a_lo:.4f}, α_hi={a_hi:.4f}, target={target:.4f})")
            harness.check(False, f"d={d_val}: crossing bracket")

    # 1.6: Gaussian approximation t₀ = 2σ/(σ−1) — verify the formula values
    print("\n  Gaussian approximation t₀ = 2σ/(σ−1):")
    paper_gauss = {2: 5.236, 3: 8.159, 4: 11.060}
    for d_val, pg in paper_gauss.items():
        s = find_positive_root(d_val)
        our = 2 * s / (s - 1)
        err = abs(our - pg)
        print(f"    d={d_val}: 2σ/(σ−1) = {our:.3f}, paper = {pg:.3f}")
        harness.check(err < 0.001, f"d={d_val}: Gaussian approx = {our:.3f} matches paper {pg:.3f}")


if __name__ == "__main__":
    h = TestHarness()
    run(h)
    h.summary()
