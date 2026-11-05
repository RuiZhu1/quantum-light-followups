"""
Skeleton verification suite for both projects.

There are no completed tests in this file. Implement tests as the corresponding
models are derived. Do not turn numerical targets from the project note into
hard-coded assertions unless the milestone explicitly calls for a regression test
after an independent derivation.

REQUIRED: record random seeds, parameter distributions, tolerances, grid sizes,
and convergence checks. A grid match is evidence, not an analytical proof.
"""

from __future__ import annotations

import numpy as np

failures = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    """Record one completed check; the student must supply meaningful `ok`."""
    global failures
    failures += not bool(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))


def test_born_and_povm() -> None:
    # REQUIRED: test positivity, normalization, Born-rule probabilities, and axes.
    raise NotImplementedError("Milestones 1-2: implement POVM and Born-rule checks")


def test_lorenz_and_majorization() -> None:
    # REQUIRED: test ordering, partial sums, equal totals, and known examples.
    # THINK: why must the least concave majorant be checked independently?
    raise NotImplementedError("Milestone 1: implement majorization checks")


def test_projective_bounds() -> None:
    # REQUIRED: compare direct-sum and tensor-product bounds against sampled states.
    # OPEN: choose convergence tests and explain why sampling does not prove optimality.
    raise NotImplementedError("Milestone 1: implement projective-bound checks")


def test_biased_povm_bounds() -> None:
    # REQUIRED: test kappa, Lambda, ordering, and Shannon/Tsallis consequences.
    # Include unequal sharpness, bias, trivial POVMs, and extreme legal parameters.
    raise NotImplementedError("Milestones 2-3: implement general POVM checks")


def test_attainment() -> None:
    # REQUIRED: cover noncommuting, commuting, trivial, tied, and degenerate cases.
    # Include a justified c=1 common-eigenvector example in higher dimension.
    raise NotImplementedError("Milestones 2-3: implement attainment checks")


def test_detector_models() -> None:
    # REQUIRED: test dark counts, click assignment, full efficiency square, and Fock
    # truncation convergence. Include analytical counterexamples when available.
    raise NotImplementedError("Milestones 2-4: implement detector regression checks")


def test_steering() -> None:
    # REQUIRED: verify conditional entropies from Born-rule joint distributions,
    # product-state false certification, and exact-Shannon versus majorization bounds.
    # THINK: why does nonviolation of a witness not prove an LHS model?
    raise NotImplementedError("Milestone 5: implement steering checks")


def test_optics() -> None:
    # REQUIRED: cover clock/shift relations, block overlap, finite-energy limits,
    # homodyne smoothing, binning bias, and state truncation convergence.
    # OPEN: choose independent analytical or numerical reference cases.
    raise NotImplementedError("Milestones 6-8: implement optical checks")


def main() -> None:
    """Run only tests that have been implemented and documented."""
    # REQUIRED: assemble the suite gradually and make every failure visible.
    # Do not report a successful full suite while these placeholders remain.
    raise NotImplementedError("Assemble verification only after implementing each milestone")
    # Suggested final behavior: sys.exit(1 if failures else 0).


if __name__ == "__main__":
    main()
