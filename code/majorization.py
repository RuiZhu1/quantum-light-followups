"""
Skeleton for majorization uncertainty relations.

Read ../LEARNING_GUIDE.md before editing. Labels have the following meaning:
REQUIRED: a constraint that must remain true and be tested.
GUIDED: a suggested route that may be replaced by a justified equivalent.
OPEN: a design or research choice for the student.
THINK: a question to answer in the milestone notes.
CHALLENGE: an optional improvement, only after the required version works.

Nothing raising NotImplementedError is implemented. Do not replace these errors with
hard-coded values from the project note or the reference manuscript.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
PAULI = (SX, SY, SZ)


def sigma_dot(v: np.ndarray) -> np.ndarray:
    """Return v . sigma for a real three-vector."""
    return v[0] * SX + v[1] * SY + v[2] * SZ


def density_matrix(r: np.ndarray) -> np.ndarray:
    """Return rho = (I + r.sigma)/2; validation is part of the tests."""
    return 0.5 * (I2 + sigma_dot(np.asarray(r, dtype=float)))


def unit(v) -> np.ndarray:
    """Normalize a nonzero real vector."""
    v = np.asarray(v, dtype=float)
    return v / np.linalg.norm(v)


def axis_in_xz_plane(angle: float) -> np.ndarray:
    """Unit Bloch vector at polar angle `angle` from +z in the x-z plane."""
    return np.array([np.sin(angle), 0.0, np.cos(angle)])


@dataclass(frozen=True)
class TwoOutcomePOVM:
    """E0 = [(1+mu)I + eta a.sigma]/2 and E1 = I-E0."""

    axis: np.ndarray
    eta: float = 1.0
    mu: float = 0.0

    def __post_init__(self):
        # REQUIRED: normalize the axis and enforce eta >= 0, |mu|+eta <= 1.
        # THINK: why are these conditions equivalent to 0 <= E0 <= I?
        raise NotImplementedError("Milestone 1: validate and initialize the POVM")

    @property
    def effects(self) -> tuple[np.ndarray, np.ndarray]:
        # REQUIRED: construct both effects and verify 0 <= E_i <= I in tests.
        raise NotImplementedError("Milestone 1: construct effects from the Bloch parametrization")

    @property
    def kappa(self) -> float:
        # GUIDED: use the largest achievable outcome probability, (1+kappa)/2.
        raise NotImplementedError("Milestone 1: derive kappa from the effects")

    def probs(self, r: np.ndarray) -> np.ndarray:
        # REQUIRED: support one Bloch vector or an array with final dimension 3.
        raise NotImplementedError("Milestone 1: implement outcome probabilities")

    def probs_born(self, r: np.ndarray) -> np.ndarray:
        # REQUIRED: compute Tr(rho E_i) independently for a Born-rule check.
        raise NotImplementedError("Milestone 1: implement the Born-rule cross-check")


def projective(axis) -> TwoOutcomePOVM:
    # GUIDED: use eta=1 and mu=0.
    raise NotImplementedError("Milestone 1: construct a sharp rank-one measurement")


def overlap_cmax(m: TwoOutcomePOVM, n: TwoOutcomePOVM) -> float:
    # THINK: why is c=(1+|a.b|)/2 only a projective qubit formula?
    raise NotImplementedError("Milestone 1: derive and implement projective overlap")


def sort_desc(v: np.ndarray) -> np.ndarray:
    """Sort entries in non-increasing order along the final axis."""
    return -np.sort(-np.asarray(v, dtype=float), axis=-1)


def lorenz(v: np.ndarray) -> np.ndarray:
    # REQUIRED: return decreasing-order partial sums without a leading zero.
    raise NotImplementedError("Milestone 1: implement Lorenz partial sums")


def is_majorized(x: np.ndarray, y: np.ndarray, tol: float = 1e-10) -> bool:
    # REQUIRED: compare equal totals and all partial sums, with documented tolerance.
    # OPEN: choose a robust floating-point comparison and explain it.
    raise NotImplementedError("Milestone 1: implement the majorization test")


def least_concave_majorant(partial_sums: np.ndarray) -> np.ndarray:
    # GUIDED: use the upper convex hull of (k,S_k), k=0,...,d.
    # OPEN: another algorithm is allowed if its output is tested independently.
    raise NotImplementedError("Milestone 1: implement the least concave majorant")


def lattice_supremum(vectors: np.ndarray) -> np.ndarray:
    # REQUIRED: combine pointwise Lorenz maxima with the least concave majorant.
    raise NotImplementedError("Milestone 1: implement the majorization-lattice supremum")


def shannon(v: np.ndarray, axis: int = -1) -> np.ndarray:
    # REQUIRED: define 0 log 0 = 0 and document whether total mass must equal 1.
    # THINK: why is the same entropy functional used for a direct sum of mass 2?
    raise NotImplementedError("Milestone 1: implement Shannon entropy")


def renyi(p: np.ndarray, alpha: float, axis: int = -1) -> np.ndarray:
    # REQUIRED: handle alpha=0, alpha=1, and alpha=infinity by their limits.
    raise NotImplementedError("Milestone 1: implement Renyi entropy and its limiting orders")


def tsallis(p: np.ndarray, q: float, axis: int = -1) -> np.ndarray:
    # REQUIRED: handle q=1 by continuity and zero probabilities correctly.
    raise NotImplementedError("Milestone 1: implement Tsallis entropy")


def binary_entropy(t: np.ndarray) -> np.ndarray:
    # GUIDED: use the Shannon functional on (t,1-t).
    raise NotImplementedError("Milestone 1: implement binary entropy")


def omega_direct_sum_projective(c: float) -> np.ndarray:
    # GUIDED: derive the vector from the four maximal direct-sum partial sums.
    raise NotImplementedError("Milestone 1: derive the projective direct-sum vector")


def omega_tensor_projective(c: float) -> np.ndarray:
    # GUIDED: use w=(1+sqrt(c))^2/4 only after deriving its origin.
    raise NotImplementedError("Milestone 1: derive the projective tensor-product vector")


def omega_direct_sum(m: TwoOutcomePOVM, n: TwoOutcomePOVM) -> np.ndarray:
    # REQUIRED: compute kappa and Lambda from the two POVMs, then prove ordering.
    # THINK: why is no flattening needed for this binary qubit case?
    raise NotImplementedError("Milestone 2: derive the general biased qubit-POVM bound")


def direct_sum(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    """Concatenate outcome distributions along the final axis."""
    return np.concatenate([p, q], axis=-1)


def tensor(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    """Form p_i q_j for every pair of outcomes."""
    return (p[..., :, None] * q[..., None, :]).reshape(*p.shape[:-1], -1)


def fibonacci_sphere(n: int) -> np.ndarray:
    """Optional utility: generate a deterministic quasi-uniform sphere grid."""
    k = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * k / n)
    theta = np.pi * (1 + 5**0.5) * k
    return np.stack([np.cos(theta)*np.sin(phi), np.sin(theta)*np.sin(phi), np.cos(phi)], axis=-1)


def random_ball(n: int, rng: np.random.Generator) -> np.ndarray:
    """Optional utility: sample Bloch vectors uniformly in the unit ball."""
    v = rng.normal(size=(n, 3))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    return v * rng.random((n, 1)) ** (1/3)


def state_grid(n_sphere: int = 20000, radii=(1.0, 0.9, 0.7, 0.5, 0.25, 0.0)) -> np.ndarray:
    """Build a sphere grid at several Bloch radii; document the discretization."""
    pts = fibonacci_sphere(n_sphere)
    return np.concatenate([r * pts for r in radii])


def numerical_omega(m: TwoOutcomePOVM, n: TwoOutcomePOVM, kind: str = "direct",
                    states: np.ndarray | None = None) -> np.ndarray:
    # REQUIRED: explain why a grid gives only a sampled lower estimate of the supremum.
    # OPEN: choose a sampling strategy and demonstrate convergence.
    raise NotImplementedError("Milestone 1: estimate the supremum from sampled states")


def great_circle(m: TwoOutcomePOVM, n: TwoOutcomePOVM, num: int = 4001) -> np.ndarray:
    # REQUIRED: handle nonparallel and commuting axes without a degenerate basis.
    raise NotImplementedError("Milestone 1: construct pure states in the measurement plane")


def min_uncertainty(m: TwoOutcomePOVM, n: TwoOutcomePOVM, func, num: int = 4001):
    # REQUIRED: justify reduction to the boundary before optimizing.
    # OPEN: choose a global strategy for multiple local minima and cusps.
    raise NotImplementedError("Milestones 4-5: implement documented entropy minimization")


def omega_direct_sum_operators(*povms: list[np.ndarray]) -> np.ndarray:
    # REQUIRED: maximize lambda_max over every subset of effects of each size.
    # GUIDED: use all combinations and the least concave majorant.
    raise NotImplementedError("Milestone 3: implement the finite-dimensional operator solver")


def big_lambda(m: TwoOutcomePOVM, n: TwoOutcomePOVM) -> float:
    # REQUIRED: evaluate the four sign choices without assuming unbiased measurements.
    raise NotImplementedError("Milestone 2: implement Lambda")


def ideal_relation_holds(m: TwoOutcomePOVM, n: TwoOutcomePOVM, tol: float = 1e-12) -> bool:
    # REQUIRED: use the criterion for the full ideal direct-sum relation only.
    # THINK: why can an individual entropy bound survive when this returns False?
    raise NotImplementedError("Milestone 2: test survival of the ideal majorization relation")


def commuting_attainment(m: TwoOutcomePOVM, n: TwoOutcomePOVM, tol: float = 1e-12) -> bool:
    # REQUIRED: derive the same-endpoint criterion and cover trivial/degenerate cases.
    # OPEN: a proof-based alternative implementation is welcome.
    raise NotImplementedError("Milestone 2: implement commuting attainment")


def werner_conditional_entropy(w: float, efficiency: float) -> float:
    # REQUIRED: derive the conditional entropy from the Born-rule joint distribution.
    # THINK: why is a witness threshold not a fundamental steering boundary?
    raise NotImplementedError("Milestone 5: implement the Werner conditional-entropy sum")


def click_mub_bound(efficiency: float) -> float:
    # GUIDED: derive the orthogonal click/no-click majorization bound from the POVM.
    raise NotImplementedError("Milestone 5: implement the majorization steering bound")


def shannon_min_in_plane(theta: float, mu: float, eta: float, nu: float | None = None,
                         zeta: float | None = None, num: int = 20001) -> float:
    # REQUIRED: justify the boundary reduction and distinguish exact and sampled minima.
    # OPEN: improve global optimization and demonstrate convergence.
    raise NotImplementedError("Milestones 4-5: compute the Shannon minimum")
