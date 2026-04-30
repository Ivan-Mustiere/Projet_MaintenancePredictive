from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_RAW_DIR = ROOT_DIR / os.getenv("DATA_RAW_DIR", "data/raw")
DATA_PROCESSED_DIR = ROOT_DIR / os.getenv("DATA_PROCESSED_DIR", "data/processed")
MODELS_DIR = ROOT_DIR / os.getenv("MODELS_DIR", "models")

TRAIN_CYCLES: int = int(os.getenv("TRAIN_CYCLES", "2000"))
RANDOM_STATE: int = int(os.getenv("RANDOM_STATE", "42"))

MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MLFLOW_EXPERIMENT_NAME: str = os.getenv("MLFLOW_EXPERIMENT_NAME", "maintenance-predictive")

SENSOR_FILES = {
    "PS2": DATA_RAW_DIR / "PS2.txt",
    "FS1": DATA_RAW_DIR / "FS1.txt",
    "profile": DATA_RAW_DIR / "profile.txt",
}

PROFILE_COLUMNS = [
    "cooler_condition",
    "valve_condition",
    "internal_pump_leakage",
    "hydraulic_accumulator",
    "stable_flag",
]
