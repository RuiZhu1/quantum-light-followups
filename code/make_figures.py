"""
Skeleton figure-generation tasks for Projects A and B.

Figures must be generated from data produced by the student's implementation.
Do not hard-code curves or numerical targets from the project note.

REQUIRED: record parameters, use readable axis labels and legends, avoid overlaps,
and save the underlying numerical data or enough metadata to reproduce the figure.
OPEN: visual design, layout, and presentation may be improved deliberately.
"""

from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "output" / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def plot_lorenz_and_gap(data: np.ndarray, **parameters):
    """Plot Lorenz curves and the estimated gap with uncertainties."""
    # REQUIRED: distinguish sampled states, analytic bounds, and finite-data error.
    raise NotImplementedError("Milestones 4-5: implement Lorenz/gap figures")


def plot_detector_map(scan_result: dict[str, np.ndarray], **parameters):
    """Plot the full efficiency-square result and any independent boundary checks."""
    # REQUIRED: include both branches and state the click-assignment model.
    # OPEN: choose a contour, region, or other clearer representation.
    raise NotImplementedError("Milestone 5: implement detector-map figures")


def plot_steering_comparison(scan_result: dict[str, np.ndarray], **parameters):
    """Compare ideal, exact-Shannon, majorization, and any other derived witness."""
    # REQUIRED: label witness thresholds as witness-specific, not fundamental limits.
    raise NotImplementedError("Milestone 5: implement steering figures")


def plot_overlap_map(overlap_result: dict[str, np.ndarray], **parameters):
    """Plot c(r) or c_E(r) with the sampling and convergence metadata."""
    # REQUIRED: do not imply continuity or irrational behavior without evidence.
    raise NotImplementedError("Milestone 7: implement overlap figures")


def plot_optical_applications(results: dict[str, np.ndarray], **parameters):
    """Plot optical-state, non-Gaussianity, and EPR-steering results separately."""
    # OPEN: design separate figures if combining them would obscure the assumptions.
    raise NotImplementedError("Milestone 8: implement optical-application figures")


def main() -> None:
    """Generate only figures whose data and models have been implemented."""
    # REQUIRED: call validated computations, not placeholder arrays.
    raise NotImplementedError("Assemble figure generation after each model is validated")


if __name__ == "__main__":
    main()
