import os
from joblib import dump, load
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

FEATURE_NAMES = [
    "LIMIT_BAL",
    "SEX",
    "EDUCATION",
    "MARRIAGE",
    "AGE",
    "PAY_0",
    "PAY_2",
    "PAY_3",
    "PAY_4",
    "PAY_5",
    "PAY_6",
    "BILL_AMT1",
    "BILL_AMT2",
    "BILL_AMT3",
    "BILL_AMT4",
    "BILL_AMT5",
    "BILL_AMT6",
    "PAY_AMT1",
    "PAY_AMT2",
    "PAY_AMT3",
    "PAY_AMT4",
    "PAY_AMT5",
    "PAY_AMT6",
]


def dataset_path() -> str:
    return os.environ.get("DATASET_PATH", "./data/UCI_Credit_Card.csv")


def model_path() -> str:
    return os.environ.get("MODEL_PATH", "./models/credit_model.joblib")


def load_dataset() -> pd.DataFrame:
    path = dataset_path()
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset no encontrado: {path}")
    return pd.read_csv(path)


def create_pipeline() -> Pipeline:
    return Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=500, class_weight="balanced")),
    ])


def preprocess_features(df: pd.DataFrame) -> pd.DataFrame:
    return df[FEATURE_NAMES].fillna(0)


def train_and_save_model() -> dict:
    df = load_dataset()
    target_name = "default.payment.next.month"
    if target_name not in df.columns:
        raise ValueError(f"Target field no encontrado: {target_name}")

    X = preprocess_features(df)
    y = df[target_name]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = create_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_prob)),
        "n_samples": int(len(X_test)),
    }

    os.makedirs(os.path.dirname(model_path()), exist_ok=True)
    dump(pipeline, model_path())
    return metrics


def load_model():
    path = model_path()
    if not os.path.exists(path):
        raise FileNotFoundError("Modelo entrenado no encontrado. Ejecuta /train o el servicio trainer.")
    return load(path)


def predict_from_features(model, features: dict) -> dict:
    payload = {key: features.get(key, 0) for key in FEATURE_NAMES}
    df = pd.DataFrame([payload])
    df = preprocess_features(df)
    proba = float(model.predict_proba(df)[0, 1])
    prediction = int(proba >= 0.5)
    return {"probability": round(proba, 4), "prediction": prediction}
