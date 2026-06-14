#!/usr/bin/env python3
"""
Shared test framework for B02 clean-room verification suite.

Provides:
  - Physical constants (φ, ρ, σ, ln2)
  - TestHarness class for pass/fail tracking and formatted output
  - Newton solver for x^d − x − 1 = 0
  - Gaussian elimination linear solver

Zero external dependencies — Python 3 stdlib only.
"""

import math
import sys


# ─── Constants ────────────────────────────────────────────────────────────────
PHI   = (1 + math.sqrt(5)) / 2                    # golden ratio, root of x²=x+1
RHO   = 1.32471795724474602596                     # plastic constant, root of x³=x+1
SIGMA = 1.22074408460575947536                     # σ-constant, root of x⁴=x+1
LN2   = math.log(2)


# ─── Test Harness ─────────────────────────────────────────────────────────────
class TestHarness:
    """Accumulates pass/fail counts across all claim modules."""

    def __init__(self):
        self.pass_count = 0
        self.fail_count = 0

    def header(self, name):
        """Print a section header."""
        print(f"\n{'═'*72}")
        print(f"  {name}")
        print(f"{'═'*72}")

    def check(self, condition, label):
        """Record a single test result."""
        if condition:
            self.pass_count += 1
            print(f"  ✅ PASS: {label}")
        else:
            self.fail_count += 1
            print(f"  ❌ FAIL: {label}")

    @property
    def total(self):
        return self.pass_count + self.fail_count

    def summary(self):
        """Print final summary and exit with appropriate code."""
        print(f"\n{'═'*72}")
        print(f"  B02 EXPERIMENT SUITE COMPLETE")
        print(f"{'═'*72}")
        print(f"  ✅ Passed: {self.pass_count}")
        print(f"  ❌ Failed: {self.fail_count}")
        print(f"  Total:    {self.total}")
        print(f"{'═'*72}")

        if self.fail_count > 0:
            print("\n  ⚠  SOME EXPERIMENTS FAILED — review output above")
            sys.exit(1)
        else:
            print("\n  All paper claims verified. Ready for submission.")
            sys.exit(0)


# ─── Newton Solver ────────────────────────────────────────────────────────────
def find_positive_root(d, tol=1e-15, max_iter=300):
    """Newton's method to find the unique positive real root of x^d - x - 1 = 0."""
    x = 1.5
    for _ in range(max_iter):
        fx = x**d - x - 1
        fpx = d * x**(d - 1) - 1
        if abs(fpx) < 1e-30:
            break
        x_new = x - fx / fpx
        if abs(x_new - x) < tol:
            x = x_new
            break
        x = x_new
    return x


# ─── Linear Solver ────────────────────────────────────────────────────────────
def solve_linear(A, b):
    """Solve Ax = b via Gaussian elimination with partial pivoting."""
    n = len(b)
    M = [A[i][:] + [b[i]] for i in range(n)]
    for col in range(n):
        max_row = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[max_row] = M[max_row], M[col]
        for row in range(col + 1, n):
            factor = M[row][col] / M[col][col]
            for j in range(col, n + 1):
                M[row][j] -= factor * M[col][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x
