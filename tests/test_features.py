import numpy as np
import pytest
from src.features.build_features import build_features, _cycle_stats


def test_build_features_shape():
    n_cycles = 10
    ps2 = np.random.rand(n_cycles, 6000)
    fs1 = np.random.rand(n_cycles, 600)
    df = build_features(ps2, fs1)
    assert len(df) == n_cycles
    assert df.shape[1] > 0


def test_build_features_no_nan():
    ps2 = np.random.rand(5, 6000)
    fs1 = np.random.rand(5, 600)
    df = build_features(ps2, fs1)
    assert not df.isnull().any().any(), "Les features ne doivent pas contenir de NaN"


def test_cycle_stats_keys():
    arr = np.random.rand(3, 100)
    stats = _cycle_stats(arr, "test")
    expected = {"test_mean", "test_std", "test_min", "test_max", "test_median"}
    assert expected.issubset(stats.keys())
