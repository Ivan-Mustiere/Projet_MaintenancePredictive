import numpy as np
import pytest
from src.data.load import load_ps2, load_fs1, load_target
from src.data.split import split_cycles
from src.utils.config import TRAIN_CYCLES


def test_ps2_shape():
    ps2 = load_ps2()
    assert ps2.ndim == 2
    assert ps2.shape[1] == 6000, "PS2 doit avoir 6000 points/cycle (100 Hz)"


def test_fs1_shape():
    fs1 = load_fs1()
    assert fs1.ndim == 2
    assert fs1.shape[1] == 600, "FS1 doit avoir 600 points/cycle (10 Hz)"


def test_target_binary():
    y = load_target()
    assert set(y.unique()).issubset({0, 1}), "La cible doit être binaire"


def test_ps2_fs1_same_n_cycles():
    ps2 = load_ps2()
    fs1 = load_fs1()
    assert ps2.shape[0] == fs1.shape[0]


def test_split_sizes():
    import pandas as pd
    n = TRAIN_CYCLES + 100
    X = pd.DataFrame(np.zeros((n, 3)))
    y = pd.Series(np.zeros(n))
    X_train, X_test, y_train, y_test = split_cycles(X, y)
    assert len(X_train) == TRAIN_CYCLES
    assert len(X_test) == 100
