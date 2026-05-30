import json
import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError


def get_database_url() -> str:
    user = os.environ.get("POSTGRES_USER", "credit")
    password = os.environ.get("POSTGRES_PASSWORD", "credit")
    host = os.environ.get("POSTGRES_HOST", "postgres")
    port = os.environ.get("POSTGRES_PORT", "5432")
    db = os.environ.get("POSTGRES_DB", "creditdb")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


engine = create_engine(get_database_url(), future=True)


def init_db() -> None:
    attempts = 0
    while attempts < 10:
        try:
            with engine.begin() as conn:
                conn.execute(
                    text(
                        """
                        CREATE TABLE IF NOT EXISTS metrics (
                            id SERIAL PRIMARY KEY,
                            accuracy DOUBLE PRECISION,
                            roc_auc DOUBLE PRECISION,
                            n_samples INTEGER,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                        """
                    )
                )
                conn.execute(
                    text(
                        """
                        CREATE TABLE IF NOT EXISTS predictions (
                            id SERIAL PRIMARY KEY,
                            input_data JSONB,
                            prediction INTEGER,
                            probability DOUBLE PRECISION,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                        """
                    )
                )
            return
        except OperationalError:
            attempts += 1
            time.sleep(2)
    raise RuntimeError("No se pudo conectar a la base de datos después de varios intentos")


def save_metrics(metrics: dict) -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                "INSERT INTO metrics (accuracy, roc_auc, n_samples) VALUES (:accuracy, :roc_auc, :n_samples)"
            ),
            metrics,
        )


def get_latest_metrics() -> dict | None:
    with engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT accuracy, roc_auc, n_samples, created_at FROM metrics ORDER BY created_at DESC LIMIT 1"
            )
        ).mappings().first()
        if not result:
            return None
        output = dict(result)
        created_at = output.get("created_at")
        if created_at is not None:
            output["created_at"] = created_at.isoformat()
        return output


def save_prediction(input_data: dict, prediction: int, probability: float) -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                "INSERT INTO predictions (input_data, prediction, probability) VALUES (CAST(:data AS JSONB), :prediction, :probability)"
            ),
            {"data": json.dumps(input_data), "prediction": prediction, "probability": probability},
        )


def get_recent_predictions(limit: int = 10) -> list[dict]:
    with engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT id, input_data, prediction, probability, created_at FROM predictions ORDER BY created_at DESC LIMIT :limit"
            ),
            {"limit": limit},
        ).mappings().all()
        rows = [dict(row) for row in result]
        for item in rows:
            if item.get("created_at") is not None:
                item["created_at"] = item["created_at"].isoformat()
        return rows
