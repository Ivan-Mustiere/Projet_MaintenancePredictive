import numpy as np
import pandas as pd
from src.utils.config import TRAIN_CYCLES


def split_cycles(
    X: pd.DataFrame, y: pd.Series
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split into train (first TRAIN_CYCLES) and test (remaining).

    The test set must never be used for training or feature selection.
    """
    X_train = X.iloc[:TRAIN_CYCLES]
    X_test = X.iloc[TRAIN_CYCLES:]
    y_train = y.iloc[:TRAIN_CYCLES]
    y_test = y.iloc[TRAIN_CYCLES:]
    return X_train, X_test, y_train, y_test
