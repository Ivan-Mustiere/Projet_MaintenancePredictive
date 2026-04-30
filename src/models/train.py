import joblib
import shutil
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
import optuna
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_validate, cross_val_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from src.utils.config import RANDOM_STATE, MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT_NAME, MODELS_DIR

optuna.logging.set_verbosity(optuna.logging.WARNING)


def build_dummy_pipeline() -> Pipeline:
    return Pipeline([
        ("clf", DummyClassifier(strategy="most_frequent", random_state=RANDOM_STATE)),
    ])


def build_baseline_pipeline() -> Pipeline:
    return Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
    ])


def build_rf_pipeline(**kwargs) -> Pipeline:
    params = dict(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1)
    params.update(kwargs)
    return Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(**params)),
    ])


def build_xgb_pipeline(**kwargs) -> Pipeline:
    params = dict(
        n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1,
        eval_metric="logloss", verbosity=0,
    )
    params.update(kwargs)
    return Pipeline([
        ("scaler", StandardScaler()),
        ("clf", XGBClassifier(**params)),
    ])


def build_lgbm_pipeline(**kwargs) -> Pipeline:
    params = dict(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1, verbosity=-1)
    params.update(kwargs)
    return Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LGBMClassifier(**params)),
    ])


def _cv_score(pipeline: Pipeline, X: pd.DataFrame, y: pd.Series) -> dict:
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    results = cross_validate(
        pipeline, X, y,
        cv=cv,
        scoring=["accuracy", "f1", "roc_auc"],
        return_train_score=False,
    )
    return {
        "cv_accuracy": float(results["test_accuracy"].mean()),
        "cv_f1": float(results["test_f1"].mean()),
        "cv_roc_auc": float(results["test_roc_auc"].mean()),
    }


def train_with_tracking(
    pipeline: Pipeline,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    run_name: str,
) -> tuple[Pipeline, dict]:
    """Train pipeline with cross-validation and log metrics to MLflow."""
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

    metrics = _cv_score(pipeline, X_train, y_train)

    with mlflow.start_run(run_name=run_name):
        mlflow.log_params(pipeline.get_params())
        mlflow.log_metrics(metrics)
        pipeline.fit(X_train, y_train)
        mlflow.sklearn.log_model(pipeline, name="model")

    return pipeline, metrics


def optimize_with_optuna(
    model_type: str,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    n_trials: int = 10,
    timeout: int = 60,
) -> dict:
    """Find best hyperparameters via Optuna for the given model type."""
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=RANDOM_STATE)

    def objective(trial: optuna.Trial) -> float:
        if model_type == "random_forest":
            pipeline = build_rf_pipeline(
                n_estimators=trial.suggest_int("n_estimators", 50, 300),
                max_depth=trial.suggest_int("max_depth", 3, 20),
                min_samples_split=trial.suggest_int("min_samples_split", 2, 20),
                min_samples_leaf=trial.suggest_int("min_samples_leaf", 1, 10),
            )
        elif model_type == "xgboost":
            pipeline = build_xgb_pipeline(
                n_estimators=trial.suggest_int("n_estimators", 50, 300),
                max_depth=trial.suggest_int("max_depth", 3, 10),
                learning_rate=trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
                subsample=trial.suggest_float("subsample", 0.6, 1.0),
                colsample_bytree=trial.suggest_float("colsample_bytree", 0.6, 1.0),
            )
        elif model_type == "lgbm":
            pipeline = build_lgbm_pipeline(
                n_estimators=trial.suggest_int("n_estimators", 50, 300),
                max_depth=trial.suggest_int("max_depth", 3, 10),
                learning_rate=trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
                num_leaves=trial.suggest_int("num_leaves", 20, 100),
                subsample=trial.suggest_float("subsample", 0.6, 1.0),
            )
        else:
            raise ValueError(f"model_type inconnu : {model_type}")

        scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="f1", n_jobs=-1)
        return float(scores.mean())

    study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=RANDOM_STATE))
    study.optimize(objective, n_trials=n_trials, timeout=timeout, show_progress_bar=False)
    return study.best_params


if __name__ == "__main__":
    from src.data.load import load_target
    from src.data.split import split_cycles
    from src.utils.config import DATA_PROCESSED_DIR

    features_path = DATA_PROCESSED_DIR / "features.parquet"
    if not features_path.exists():
        raise FileNotFoundError(
            f"{features_path} introuvable — lancer d'abord : ./run.sh features"
        )

    print("Chargement des features...")
    X = pd.read_parquet(features_path)
    y = load_target()
    X_train, _, y_train, _ = split_cycles(X, y)
    print(f"  Train : {X_train.shape}  |  classes : {y_train.value_counts().to_dict()}")

    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    results = {}

    # ---- 1. Modèles de base ----
    for name, pipeline in [
        ("dummy",         build_dummy_pipeline()),
        ("baseline",      build_baseline_pipeline()),
        ("random_forest", build_rf_pipeline()),
        ("xgboost",       build_xgb_pipeline()),
        ("lgbm",          build_lgbm_pipeline()),
    ]:
        print(f"\nEntraînement : {name}...")
        trained, metrics = train_with_tracking(pipeline, X_train, y_train, run_name=name)
        joblib.dump(trained, MODELS_DIR / f"{name}.joblib")
        results[name] = metrics
        print(f"  F1={metrics['cv_f1']:.4f}  AUC={metrics['cv_roc_auc']:.4f}")

    # ---- 2. Optuna sur le meilleur modèle ----
    best_name = max(
        (n for n in results if n not in ("dummy", "baseline")),
        key=lambda n: results[n]["cv_f1"],
    )
    print(f"\nOptimisation Optuna sur : {best_name} (30 trials)...")
    best_params = optimize_with_optuna(best_name, X_train, y_train, n_trials=30)
    print(f"  Meilleurs paramètres : {best_params}")

    builders = {"random_forest": build_rf_pipeline, "xgboost": build_xgb_pipeline, "lgbm": build_lgbm_pipeline}
    tuned_pipeline, tuned_metrics = train_with_tracking(
        builders[best_name](**best_params), X_train, y_train, run_name=f"{best_name}_tuned"
    )
    joblib.dump(tuned_pipeline, MODELS_DIR / "best_model.joblib")
    print(f"  Tuned — F1={tuned_metrics['cv_f1']:.4f}  AUC={tuned_metrics['cv_roc_auc']:.4f}")

    # ---- 3. Modèle par défaut pour l'API ----
    shutil.copy(MODELS_DIR / "best_model.joblib", MODELS_DIR / "model.joblib")

    # ---- Résumé ----
    print("\n=== Résumé ===")
    all_results = {**results, f"{best_name}_tuned": tuned_metrics}
    for name, m in sorted(all_results.items(), key=lambda x: x[1]["cv_f1"], reverse=True):
        print(f"  {name:<20} F1={m['cv_f1']:.4f}  AUC={m['cv_roc_auc']:.4f}  Acc={m['cv_accuracy']:.4f}")
    print(f"\nModèle déployé : {MODELS_DIR / 'model.joblib'}")
