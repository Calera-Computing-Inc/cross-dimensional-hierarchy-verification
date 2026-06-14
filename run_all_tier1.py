#!/usr/bin/env python3
"""
B02 Paper — Tier 1 Experiment Suite
Pure mathematics validation (no codebase or third-party dependencies required)

Validates all algebraic, numerical, spectral, and combinatorial claims in:
  "The x^d = x + 1 Hierarchy: Cross-Dimensional Spectral Validation
   on A_d Root Lattices"

This is a CLEAN-ROOM implementation: only Python 3 stdlib is used.
No numpy, no scipy, no external dependencies.

Usage:
  python3 run_all_tier1.py              # Run all claims
  python3 -m tests.test_claim0_roots    # Run individual claim
"""

from tests.framework import TestHarness
from tests import (
    test_claim0_roots,
    test_claim1_spectral,
    test_claim2_recurrence,
    test_claim3_asymptotics,
    test_claim4_hyperbox,
    test_bonus_consistency,
)


def main():
    harness = TestHarness()

    modules = [
        test_claim0_roots,
        test_claim1_spectral,
        test_claim2_recurrence,
        test_claim3_asymptotics,
        test_claim4_hyperbox,
        test_bonus_consistency,
    ]

    for module in modules:
        module.run(harness)

    harness.summary()


if __name__ == "__main__":
    main()
