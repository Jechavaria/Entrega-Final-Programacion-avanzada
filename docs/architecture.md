# Arquitectura del Sistema

## Diseño de servicios

- `backend`: API REST con FastAPI. Gestiona inferencia, persistencia de métricas y predicciones, y expone endpoints para entrenamiento.
- `trainer`: servicio encargado de ejecutar el pipeline de entrenamiento y guardar el modelo en el volumen compartido.
- `postgres`: almacenaje persistente de métricas y resultados de inferencia.
- `frontend`: interfaz React para consumir el modelo y mostrar resultados.

## Flujo de ML

1. El dataset `UCI_Credit_Card.csv` se comparte por bind mount en los contenedores de backend y entrenamiento.
2. El servicio `trainer` carga el dataset, realiza preprocesamiento y entrena un modelo de regresión logística.
3. El modelo se guarda en `./models/credit_model.joblib`.
4. El backend carga el modelo y expone:
   - `POST /train`
   - `POST /predict`
   - `GET /metrics`
   - `GET /predictions`
5. Los resultados y métricas se persisten en PostgreSQL.
6. El frontend consume los endpoints y ofrece control del pipeline.

## Persistencia

- Dataset: bind mount desde el host.
- Modelo entrenado: volumen local `./models`.
- Métricas y predicciones: PostgreSQL.

## Ejecución con Docker Compose

- `docker compose up --build`
- Frontend: `http://localhost:3000`
- API docs: `http://localhost:8000/docs`
