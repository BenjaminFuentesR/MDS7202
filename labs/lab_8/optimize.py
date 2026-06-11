import os
import pickle
from datetime import datetime
from pathlib import Path

import mlflow
import mlflow.sklearn
import mlflow.xgboost
import optuna
import pandas as pd
from optuna.visualization import plot_optimization_history, plot_param_importances
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

optuna.logging.set_verbosity(optuna.logging.WARNING)


os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"

base_dir = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
mlruns_path = base_dir / "mlruns"

mlflow.set_tracking_uri(f"file:///{mlruns_path.as_posix()}")


EXPERIMENT_NAME = "Water Potability XGBoost"
RANDOM_STATE = 42


def load_data():
    df = pd.read_csv("water_potability.csv")
    df = df.dropna()
    X = df.drop(columns=["Potability"])
    y = df["Potability"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test, y_train, y_test


def get_best_model(experiment_id):
    runs = mlflow.search_runs(experiment_id)
    best_model_id = runs.sort_values("metrics.valid_f1", ascending=False)["run_id"].iloc[0]
    best_model = mlflow.xgboost.load_model("runs:/" + best_model_id + "/model")
    return best_model


def optimize_model():
    X_train, X_test, y_train, y_test = load_data()

    mlflow.set_experiment(EXPERIMENT_NAME)
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

    def objective(trial):
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 50, 300),
            "max_depth": trial.suggest_int("max_depth", 3, 10),
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
            "subsample": trial.suggest_float("subsample", 0.5, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
            "reg_alpha": trial.suggest_float("reg_alpha", 1e-8, 10.0, log=True),
            "reg_lambda": trial.suggest_float("reg_lambda", 1e-8, 10.0, log=True),
        }

        run_name = f"XGBoost lr={params['learning_rate']:.4f} depth={params['max_depth']}"

        mlflow.autolog(log_models=True)
        with mlflow.start_run(run_name=run_name):
            model = XGBClassifier(**params, random_state=RANDOM_STATE, eval_metric="logloss", verbosity=0)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            f1 = f1_score(y_test, y_pred)
            mlflow.log_metric("valid_f1", f1)

        return f1

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=20, show_progress_bar=True)

    print(f"Mejor F1: {study.best_value:.4f}")
    print(f"Mejores hiperparámetros: {study.best_params}")

    # Guardar plots de Optuna
    os.makedirs("plots", exist_ok=True)
    plot_optimization_history(study).write_image("plots/optimization_history.png")
    plot_param_importances(study).write_image("plots/feature_importance.png")
    print("Plots guardados en plots/")

    # Guardar mejor modelo
    best_model = get_best_model(experiment.experiment_id)
    os.makedirs("models", exist_ok=True)
    fecha = datetime.now().strftime("%Y%m%d")
    model_path = f"models/xgb_{fecha}.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(best_model, f)
    print(f"Modelo guardado en {model_path}")

    # Generar requirements.txt
    os.system("uv export --no-hashes --no-color > requirements.txt")
    print("requirements.txt generado con uv export")


if __name__ == "__main__":
    optimize_model()
