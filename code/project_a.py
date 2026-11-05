"""
Project A skeleton: detector-aware photon measurements and steering.

Read ../LEARNING_GUIDE.md and the Project A sections of the project note first.
The suggested interfaces are GUIDED, not mandatory. A different interface is
welcome if it improves the model and is documented and tested.
"""

from __future__ import annotations

import numpy as np


def single_photon_effects(eta_h: float, eta_v: float, dark_h: float, dark_v: float,
                          double_to_h: float = 0.5) -> tuple[np.ndarray, np.ndarray]:
    """
    Return the two H/V effects for the calibrated single-photon analyzer.

    REQUIRED: derive the effects from detector outcomes, including dark counts,
    no-click splitting, and double-click assignment. Verify positivity,
    normalization, and the no-dark-count limit independently.

    THINK: which click-assignment rules are physical detector models and which are
    classical post-processing choices?
    """
    raise NotImplementedError("Milestone 2: derive and implement single-photon effects")


def rotate_effect(effect: np.ndarray, theta: float) -> np.ndarray:
    """
    Rotate an effect to another analyzer setting.

    GUIDED: use the spin or polarization rotation appropriate to the chosen basis.

    OPEN: derive the rotation in a different but equivalent basis if it makes the
    experiment clearer. Verify unitarity and the zero-angle limit.
    """
    raise NotImplementedError("Milestone 3: implement analyzer rotation")


def fock_effects(max_photons: int, eta_h: float, eta_v: float, dark_h: float,
                 dark_v: float, double_to_h: float = 0.5) -> list[np.ndarray]:
    """
    Return block-diagonal effects for a truncated photon-number model.

    REQUIRED: derive each photon-number block and document truncation. Check that
    each block is a valid effect and that the full truncated operator respects the
    chosen measurement model.

    OPEN: choose a block representation that makes convergence and computation
    efficient. Do not assume that a single-photon bound remains valid.
    """
    raise NotImplementedError("Milestone 3: implement Fock-space effects")


def fock_partial_sums(effects: list[np.ndarray], rotated_effects: list[np.ndarray]) -> np.ndarray:
    """
    Compute the maximal partial sums for a pair of block-structured measurements.

    REQUIRED: use the general operator-level construction and check truncation
    convergence. A table from the project note is a comparison target, not an input.

    THINK: what additional assumptions would make a single-photon correction safe?
    """
    raise NotImplementedError("Milestone 3: compute Fock-space partial sums")


def simulate_counts(probabilities: np.ndarray, shots: int,
                    rng: np.random.Generator) -> np.ndarray:
    """
    Simulate counts from outcome probabilities.

    REQUIRED: use the probabilities of the implemented physical model, normalize
    correctly, and compare sampled frequencies with analytic probabilities.

    OPEN: choose a sampling method and document variance and convergence.
    """
    raise NotImplementedError("Milestone 4: implement Monte Carlo count simulation")


def bootstrap_frequencies(counts: np.ndarray, rng: np.random.Generator,
                          repeats: int = 1000) -> np.ndarray:
    """
    Return bootstrap frequency samples for uncertainty analysis.

    GUIDED: use resampled counts and a percentile or another justified interval.

    OPEN: a different uncertainty estimator is allowed if calibrated and documented.
    """
    raise NotImplementedError("Milestone 4: implement bootstrap uncertainty analysis")


def estimate_non_attainment_gap(probabilities: np.ndarray, bound: np.ndarray) -> float:
    """
    Estimate the closest-state Lorenz gap from sampled states.

    REQUIRED: distinguish a finite-sample estimate from a proof of global
    non-attainment. Report the state family, optimization, and statistical error.

    OPEN: choose the optimization and uncertainty propagation.
    """
    raise NotImplementedError("Milestone 5: estimate the non-attainment gap")


def detector_mismatch_scan(efficiencies_h: np.ndarray, efficiencies_v: np.ndarray,
                           **model_parameters) -> dict[str, np.ndarray]:
    """
    Evaluate ideal-relation and entropic survival over the full efficiency square.

    REQUIRED: scan both low- and high-efficiency branches and check detector-label
    symmetry. Do not restrict the scan to eta_V <= eta_H without saying so.

    OPEN: choose analytic, grid, or adaptive boundary refinement, with convergence.
    """
    raise NotImplementedError("Milestone 5: implement the full detector-mismatch scan")


def steering_conditional_entropy(joint_probabilities: np.ndarray) -> float:
    """
    Compute the conditional entropy sum from measured or simulated joint outcomes.

    REQUIRED: derive the conditional distributions and normalize them correctly.
    Do not infer steering merely from failure of an ideal-detector relation.

    THINK: what calibration and no-post-selection assumptions are being used?
    """
    raise NotImplementedError("Milestone 5: implement conditional steering entropies")


def steering_scan(efficiencies: np.ndarray, state_parameters: np.ndarray,
                  **model_parameters) -> dict[str, np.ndarray]:
    """
    Compare ideal, exact-Shannon, and majorization steering criteria.

    REQUIRED: distinguish all three levels and include product, Bell, and Werner
    examples. A witness threshold is only a threshold of that witness.

    OPEN: choose a scan or root-finding strategy and document convergence.

    CHALLENGE: after the required comparison works, investigate whether a better
    witness or model can be justified without overclaiming its scope.
    """
    raise NotImplementedError("Milestone 5: implement the steering comparison")
