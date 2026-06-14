# Cross-Dimensional Hierarchy Verification

**Clean-room verification suite** for the paper:

> **"The x^d = x + 1 Hierarchy: Cross-Dimensional Spectral Validation on A_d Root Lattices"**
> Casey Lee Race, Calera Computing, Inc.
> [DOI: 10.5281/zenodo.20692936](https://doi.org/10.5281/zenodo.20692936) *(Zenodo preprint, 2026)*

This repository contains the clean-room verification suite that reproduces **every numerical claim** in the paper using **zero external dependencies**.

---

## Quick Start

```bash
# Run all 135 tests
python3 run_all_tier1.py

# Run individual claim modules
python3 -m tests.test_claim0_roots
python3 -m tests.test_claim1_spectral
python3 -m tests.test_claim2_recurrence
python3 -m tests.test_claim3_asymptotics
python3 -m tests.test_claim4_hyperbox
python3 -m tests.test_bonus_consistency
```

No virtual environment, no `pip install`, no NumPy required.


## Project Structure

```
cross-dimensional-hierarchy-verification/
├── run_all_tier1.py                       # Entry point — runs all claims
├── tests/
│   ├── __init__.py
│   ├── framework.py                       # Shared: constants, TestHarness, Newton solver
│   ├── test_claim0_roots.py               # Polynomial Roots σ_d (21 tests)
│   ├── test_claim1_spectral.py            # Heat-Kernel Spectral Analysis (21 tests)
│   ├── test_claim2_recurrence.py          # Sparse Recurrence (26 tests)
│   ├── test_claim3_asymptotics.py         # Asymptotic Expansion + Lagrange (25 tests)
│   ├── test_claim4_hyperbox.py            # Van der Laan Subdivision (34 tests)
│   └── test_bonus_consistency.py          # Cross-Cutting Checks (8 tests)
├── LICENSE
└── README.md
```

## Design Principles

- **Zero external dependencies** — uses only Python 3 stdlib (`math`, `sys`, `itertools`, `collections`, `fractions`)
- **No codebase coupling** — validates paper mathematics independently, with no reference to any production system
- **Modular** — each claim is independently runnable via `python3 -m tests.<module>`
- **Deterministic** — every run produces identical results
- **Self-contained Newton solver** — computes σ_d from scratch via Newton's method on x^d − x − 1 = 0
- **Exact arithmetic** — Lagrange inversion coefficients computed using Python's `fractions.Fraction` for zero rounding error

---

## What's Tested

| Module | Claim | Tests | Description |
|:---|:---|:---:|:---|
| `test_claim0_roots` | Polynomial Roots σ_d | 21 | φ, ρ, σ constants; residuals d=2..10; Table 1 |
| `test_claim1_spectral` | Heat-Kernel Spectral | 21 | P̂(**k**) normalization, α(t) boundary/monotonicity, t₀ crossing, Gaussian approx |
| `test_claim2_recurrence` | Sparse Recurrence | 26 | Ratio convergence d=2..15; cutting identity |
| `test_claim3_asymptotics` | Asymptotic Expansion | 25 | Leading term, exact c₂–c₄, Lagrange inversion n=1..8, 8-term accuracy |
| `test_claim4_hyperbox` | Van der Laan Subdivision | 34 | Self-similarity, BFS enumeration, volume conservation, ergodicity |
| `test_bonus_consistency` | Cross-Cutting Checks | 8 | Algebraic identities, semantic octave, monotonic decrease |
| | **Total** | **135** | |

---

## Related Work

- **Companion paper (B01):** [*The σ-Constant: A Universal Algebraic Invariant for Energy Propagation in d-Dimensional Simplicial Lattices*](https://doi.org/10.5281/zenodo.20350425) — establishes σ₄ ≈ 1.22074 as the decay constant for the A₄ root lattice
- **B01 verification:** [github.com/Calera-Computing-Inc/sigma-constant-verification](https://github.com/Calera-Computing-Inc/sigma-constant-verification)

---

## License

MIT License — see [LICENSE](LICENSE).

## Citation

If you use this verification suite in your work, please cite the paper:

```bibtex
@misc{race2026hierarchy,
  author       = {Race, Casey Lee},
  title        = {The $x^d = x + 1$ Hierarchy: Cross-Dimensional Spectral
                  Validation on $A_d$ Root Lattices},
  year         = {2026},
  howpublished = {Zenodo preprint},
  note         = {DOI: 10.5281/zenodo.20692936}
}
```
