# Documentación técnica (resumen)

## Resumen
Proyecto ML para predicción de impago con servicios desacoplados: `postgres` (persistencia), `backend` (API FastAPI + DB), `trainer` (proceso de entrenamiento) y `frontend` (React).

## Arquitectura
- Postgres: almacena métricas y predicciones (JSONB). Puerto interno: 5432.
- Backend (FastAPI / Uvicorn): expone API REST en `http://localhost:8000`.
- Trainer: proceso one-shot que ejecuta `train.py` y guarda el modelo en `/app/models/credit_model.joblib`.
- Frontend (Vite + React): UI en `http://localhost:3000` que consume la API.

Servicios orquestados por `docker compose` (ver `docker-compose.yml`). Volúmenes: `postgres_data`, `./models` y `./UCI_Credit_Card.csv` montado en el contenedor del backend.

## Flujo general / pipeline
1. Entrenamiento
   - `POST /train` o ejecución del servicio `trainer` comporta: carga de `UCI_Credit_Card.csv`, entrenamiento del pipeline, cálculo de métricas (accuracy, roc_auc) y guardado del modelo en `/app/models`.
   - Resultado: métricas persistidas en la tabla `metrics` y artefacto `credit_model.joblib` creado.

2. Predicción
   - Cliente (frontend o curl) envía features JSON a `POST /predict`.
   - El backend carga el modelo (si existe), calcula `prediction` y `probability`, guarda un registro en la tabla `predictions` (campo `input_data` como JSONB) y devuelve el resultado.

3. Consulta
   - `GET /metrics`: devuelve las métricas más recientes (con `created_at` en ISO8601).
   - `GET /predictions`: devuelve las predicciones guardadas (lista con `id`, `input_data`, `prediction`, `probability`, `created_at`).

## Endpoints principales (resumen)
- `GET /health` → sanity check. Respuesta esperada: `{"status":"ok", "dataset":..., "model_path":...}`
- `POST /train` → entrena y persiste métricas. Devuelve objeto `MetricsResponse`.
- `POST /predict` → recibe `PredictRequest` (campos numéricos), devuelve `{"prediction": int, "probability": float}` y guarda el registro.
- `GET /metrics` → `MetricsResponse` con `created_at` ISO.
- `GET /predictions` → lista de objetos `PredictionRecord`.

## Ejecución local (Docker Compose)
En la raíz del proyecto (`c:\Users\david\Documents\Firu`):

```cmd
docker compose up --build
```

Comandos útiles para pruebas rápidas (desde Windows `cmd`):

```cmd
curl.exe http://localhost:8000/health
curl.exe -X POST http://localhost:8000/train
curl.exe -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d @predict_input.json
curl.exe http://localhost:8000/metrics
curl.exe http://localhost:8000/predictions
```

Front-end (se exponerá automáticamente en `http://localhost:3000` cuando `docker compose` levante el servicio). Alternativa para desarrollo sin Docker:

```cmd
# Backend (desde carpeta backend)
uvicorn app:app --host 0.0.0.0 --port 8000

# Frontend (desde carpeta frontend)
npm install
npm run dev
```

## Qué verificar para considerar el proyecto 100% funcional
- `docker compose up --build` sin errores y servicios activos.
- `GET /health` responde correctamente.
- `POST /train` devuelve métricas y crea `credit_model.joblib` en `./models`.
- `POST /predict` devuelve `prediction` y `probability` y `GET /predictions` muestra el registro.
- Frontend en `http://localhost:3000` permite entrenar y predecir desde la UI.

## Notas y detalles técnicos
- La tabla `predictions.input_data` se guarda como JSONB; al insertar desde SQLAlchemy se serializa con `json.dumps(...)` y se hace `CAST(... AS JSONB)` en la consulta.
- Los timestamps se devuelven serializados con `isoformat()` desde `backend/db.py`.
- El modelo se guarda/lee con `joblib` en `/app/models/credit_model.joblib`.

---
Documento breve generado automáticamente. Para ampliar, actualizar `docs/pruebas.md` o `README.md`.
