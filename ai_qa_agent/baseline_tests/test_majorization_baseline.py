"""Baseline tests for the subset of majorization.py implemented for the demo."""

from __future__ import annotations

import numpy as np
import pytest

from ai_qa_agent.loader import load_majorization

majorization = load_majorization()
binary_entropy = majorization.binary_entropy
is_majorized = majorization.is_majorized
lorenz = majorization.lorenz
shannon = majorization.shannon


class TestLorenz:
    def test_uniform_distribution(self):
        v = np.array([0.25, 0.25, 0.25, 0.25])
        expected = np.array([0.25, 0.5, 0.75, 1.0])
        assert np.allclose(lorenz(v), expected)

    def test_sorted_descending(self):
        v = np.array([0.1, 0.9])
        expected = np.array([0.9, 1.0])
        assert np.allclose(lorenz(v), expected)

    def test_batch_axis(self):
        vs = np.array([[0.5, 0.5], [0.1, 0.9]])
        expected = np.array([[0.5, 1.0], [0.9, 1.0]])
        assert np.allclose(lorenz(vs), expected)


class TestIsMajorized:
    def test_uniform_majorized_by_peaked(self):
        uniform = np.array([0.25, 0.25, 0.25, 0.25])
        peaked = np.array([1.0, 0.0, 0.0, 0.0])
        assert is_majorized(uniform, peaked)
        assert not is_majorized(peaked, uniform)

    def test_equal_vectors(self):
        v = np.array([0.2, 0.3, 0.5])
        assert is_majorized(v, v)

    def test_different_totals(self):
        x = np.array([0.5, 0.5])
        y = np.array([1.0, 1.0])
        assert not is_majorized(x, y)


class TestShannon:
    def test_uniform_two_outcomes(self):
        v = np.array([0.5, 0.5])
        assert shannon(v) == pytest.approx(np.log(2))

    def test_certainty(self):
        v = np.array([1.0, 0.0, 0.0])
        assert shannon(v) == pytest.approx(0.0)

    def test_zero_probability_handled(self):
        v = np.array([0.0, 1.0])
        assert shannon(v) == pytest.approx(0.0)


class TestBinaryEntropy:
    def test_fair_coin(self):
        assert binary_entropy(0.5) == pytest.approx(np.log(2))

    def test_certain_outcomes(self):
        assert binary_entropy(0.0) == pytest.approx(0.0)
        assert binary_entropy(1.0) == pytest.approx(0.0)

    def test_array_input(self):
        ts = np.array([0.0, 0.5, 1.0])
        expected = np.array([0.0, np.log(2), 0.0])
        assert np.allclose(binary_entropy(ts), expected)
