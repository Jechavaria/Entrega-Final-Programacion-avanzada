# Plataforma de ML con Docker Compose

Este proyecto implementa un pipeline de Machine Learning para el dataset `UCI_Credit_Card.csv`.
La arquitectura usa servicios independientes para backend, entrenamiento, frontend y base de datos.

## Componentes

- `backend`: API REST con FastAPI para entrenamiento, inferencia y persistencia.
- `trainer`: servicio de entrenamiento que genera el modelo y guarda métricas.
- `postgres`: base de datos PostgreSQL para métricas y predicciones.
- `frontend`: aplicación React para interactuar con el pipeline.

## Arquitectura

- Persistencia del dataset: se monta en el contenedor `backend` y `trainer`.
- Modelo entrenado: se guarda en el volumen local `./models`.
- Métricas y predicciones: se almacenan en PostgreSQL.
- API de inferencia: `POST /predict`.
- API de entrenamiento: `POST /train`.

## Ejecución

1. Construir y levantar los servicios:

```bash
docker compose up --build
```

2. Acceder al frontend en:

```bash
http://localhost:3000
```

3. Acceder a la API directamente en:

```bash
http://localhost:8000/docs
```

## Flujo principal

1. El servicio `trainer` carga el dataset, preprocesa, entrena un modelo de regresión logística y guarda el modelo.
2. El backend expone endpoint para inferencia y visualización de métricas.
3. El frontend consume el modelo y muestra resultados de predicción.

## Endpoints clave

- `POST /train`: entrena el modelo y guarda métricas.
- `POST /predict`: recibe un registro y devuelve predicción.
- `GET /metrics`: muestra métricas de la última sesión de entrenamiento.
- `GET /predictions`: muestra las predicciones recientes.
