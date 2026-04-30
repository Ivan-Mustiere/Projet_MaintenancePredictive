import numpy as np
import pandas as pd
from pathlib import Path
from src.utils.config import SENSOR_FILES, PROFILE_COLUMNS


def load_sensor(path: Path, n_points: int) -> np.ndarray:
    """Load a sensor file. Returns array of shape (n_cycles, n_points)."""
    return np.loadtxt(path)


def load_ps2() -> np.ndarray:
    """Load PS2 pressure sensor — 6000 points/cycle at 100 Hz."""
    return load_sensor(SENSOR_FILES["PS2"], n_points=6000)


def load_fs1() -> np.ndarray:
    """Load FS1 flow sensor — 600 points/cycle at 10 Hz."""
    return load_sensor(SENSOR_FILES["FS1"], n_points=600)


def load_profile() -> pd.DataFrame:
    """Load profile file containing target labels and system conditions."""
    df = pd.read_csv(SENSOR_FILES["profile"], sep="\t", header=None, names=PROFILE_COLUMNS)
    df.index.name = "cycle_id"
    return df


def load_target() -> pd.Series:
    """Return binary target: 1 = valve optimal (100%), 0 = non-optimal."""
    profile = load_profile()
    return (profile["valve_condition"] == 100).astype(int).rename("target")
