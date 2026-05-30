# Instrucciones de prueba

Este documento describe cómo verificar que el proyecto funciona correctamente.

## 1. Preparación

1. Abre una terminal en `C:\Users\david\Documents\Firu`.
2. Si tienes Docker instalado, ejecuta:

```bash
docker compose up --build
```

3. Si no tienes Docker, puedes ejecutar el backend localmente:

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

> En ambos casos, el backend debe quedar disponible en `http://localhost:8000`.

## 2. Prueba de estado del sistema

1. Abre tu navegador o usa `curl`:

```bash
curl http://localhost:8000/health
```

2. Resultado esperado:
- Respuesta JSON con `status: "ok"`.
- Rutas para `dataset` y `model_path`.

## 3. Probar la documentación Swagger

1. Abre en el navegador:

```text
http://localhost:8000/docs
```

2. Resultado esperado:
- La interfaz de Swagger muestra los endpoints `POST /train`, `POST /predict`, `GET /metrics`, `GET /predictions`.

## 4. Entrenamiento del modelo

1. Ejecuta el endpoint de entrenamiento:

```bash
curl -X POST http://localhost:8000/train
```

2. Resultado esperado:
- JSON con métricas `accuracy`, `roc_auc`, `n_samples` y `created_at`.
- El archivo `models/credit_model.joblib` deberá crearse en el proyecto.
- Se insertan métricas en la base de datos.

## 5. Inferencia / predicción

1. Ejecuta el endpoint de predicción con datos de ejemplo:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d "{\"LIMIT_BAL\":20000,\"SEX\":2,\"EDUCATION\":2,\"MARRIAGE\":1,\"AGE\":30,\"PAY_0\":0,\"PAY_2\":0,\"PAY_3\":0,\"PAY_4\":0,\"PAY_5\":0,\"PAY_6\":0,\"BILL_AMT1\":0,\"BILL_AMT2\":0,\"BILL_AMT3\":0,\"BILL_AMT4\":0,\"BILL_AMT5\":0,\"BILL_AMT6\":0,\"PAY_AMT1\":0,\"PAY_AMT2\":0,\"PAY_AMT3\":0,\"PAY_AMT4\":0,\"PAY_AMT5\":0,\"PAY_AMT6\":0}"
```

2. Resultado esperado:
- JSON con `prediction` y `probability`.
- El resultado se debe guardar en la tabla `predictions`.

## 6. Verificar métricas guardadas

1. Ejecuta:

```bash
curl http://localhost:8000/metrics
```

2. Resultado esperado:
- JSON con la última métrica guardada.

## 7. Verificar predicciones guardadas

1. Ejecuta:

```bash
curl http://localhost:8000/predictions
```

2. Resultado esperado:
- JSON con las predicciones recientes, incluyendo `id`, `input_data`, `prediction`, `probability`, `created_at`.

## 8. Probar el frontend

1. Abre en el navegador:

```text
http://localhost:3000
```

2. Pruebas a realizar:
- Pulsar `Entrenar modelo`.
- Confirmar que aparecen métricas actualizadas.
- Llenar el formulario de predicción y enviar.
- Confirmar que muestra `Predicción` y `Probabilidad`.
- Revisar que aparecen registros en `Predicciones recientes`.

## 9. Prueba de persistencia

1. Detén los contenedores con `Ctrl+C` y ejecuta:

```bash
docker compose down
```

2. Vuelve a levantarlos:

```bash
docker compose up
```

3. Verifica nuevamente `GET /metrics` y `GET /predictions`.

4. Resultado esperado:
- Las métricas y predicciones previas siguen disponibles si la base de datos persistió correctamente.

## 10. Resultados esperados generales

- El proyecto debe generar un modelo en `models/credit_model.joblib`.
- El endpoint `POST /train` debe producir métricas y guardarlas.
- El endpoint `POST /predict` debe devolver una predicción válida.
- El frontend debe ser capaz de entrenar, predecir y mostrar datos.
- La persistencia de métricas y predicciones debe funcionar con PostgreSQL.
