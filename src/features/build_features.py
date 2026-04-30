import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats


def _cycle_stats(arr: np.ndarray, prefix: str) -> dict:
    """Compute statistical features for one sensor array (n_cycles, n_points)."""
    return {
        f"{prefix}_mean": arr.mean(axis=1),
        f"{prefix}_std": arr.std(axis=1),
        f"{prefix}_min": arr.min(axis=1),
        f"{prefix}_max": arr.max(axis=1),
        f"{prefix}_median": np.median(arr, axis=1),
        f"{prefix}_q25": np.percentile(arr, 25, axis=1),
        f"{prefix}_q75": np.percentile(arr, 75, axis=1),
        f"{prefix}_iqr": np.percentile(arr, 75, axis=1) - np.percentile(arr, 25, axis=1),
        f"{prefix}_skew": stats.skew(arr, axis=1),
        f"{prefix}_kurt": stats.kurtosis(arr, axis=1),
        f"{prefix}_rms": np.sqrt((arr**2).mean(axis=1)),
        f"{prefix}_range": arr.max(axis=1) - arr.min(axis=1),
    }


def _fft_features(arr: np.ndarray, prefix: str, n_components: int = 10) -> dict:
    """Compute FFT spectral energy features for each cycle."""
    fft_vals = np.abs(np.fft.rfft(arr, axis=1))
    features = {}
    for i in range(n_components):
        features[f"{prefix}_fft_{i}"] = fft_vals[:, i]
    features[f"{prefix}_spectral_energy"] = (fft_vals**2).sum(axis=1)
    return features


def build_features(ps2: np.ndarray, fs1: np.ndarray) -> pd.DataFrame:
    """Build feature matrix from PS2 and FS1 sensor arrays.

    Aggregates each sensor by cycle to avoid raw time-series concatenation
    across incompatible sampling rates (100 Hz vs 10 Hz).
    """
    features: dict = {}
    features.update(_cycle_stats(ps2, "ps2"))
    features.update(_cycle_stats(fs1, "fs1"))
    features.update(_fft_features(ps2, "ps2", n_components=10))
    features.update(_fft_features(fs1, "fs1", n_components=5))

    df = pd.DataFrame(features)
    df.index.name = "cycle_id"
    return df


if __name__ == "__main__":
    from src.data.load import load_ps2, load_fs1
    from src.utils.config import DATA_PROCESSED_DIR

    print("Chargement des capteurs...")
    ps2 = load_ps2()
    fs1 = load_fs1()
    print(f"  PS2 : {ps2.shape}  FS1 : {fs1.shape}")

    print("Construction des features...")
    df = build_features(ps2, fs1)
    print(f"  Feature matrix : {df.shape} ({df.shape[1]} features, {df.shape[0]} cycles)")

    out = Path(DATA_PROCESSED_DIR) / "features.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out)
    print(f"  Sauvegardé : {out}")
