# Housing Price Prediction

Sistema de valoracion immobiliaria basado en Machine Learning. Entrena un modelo Random Forest Regressor sobre datos de viviendas, lo expone como API REST con FastAPI y lo consume desde un dashboard en Streamlit.

Proyecto academico de Mineria de Datos.

## Indice

- [Arquitectura](#arquitectura)
- [Requerimientos](#requerimientos)
- [Instalacion](#instalacion)
- [Ejecucion](#ejecucion)
- [API](#api)
- [Modelo](#modelo)
- [Resultados](#resultados)
- [Pruebas](#pruebas)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Documentacion adicional](#documentacion-adicional)

## Arquitectura

```
data/Housing.csv
        |
        v
src/train.py  --->  models/model.pkl
                       |
                       v
                  src/app.py  (FastAPI, puerto 8001)
                       |
                       v
                dashboard/app.py  (Streamlit, puerto 8501)
```

El dashboard no carga el modelo por su cuenta: consume la API, de modo que existe una unica ruta para obtener predicciones. La API es ademas la que ejecuta el analisis exploratorio bajo demanda.

## Requerimientos

- Python 3.9 o superior (probado en 3.13)
- Las dependencias se instalan desde `requirements.txt`

## Instalacion

```bash
git clone https://github.com/Bhalde2/trabajo_mineria.git
cd trabajo_mineria
pip install -r requirements.txt
```

El dataset (`data/Housing.csv`, 1000 registros) viene en el repositorio, por lo que no es necesario generar datos para ejecutar el sistema.

## Ejecucion

Los dos servicios se levantan en terminales separadas, siempre desde la raiz del repositorio.

Terminal 1, API:

```bash
python src/app.py
```

Documentacion interactiva de la API: <http://localhost:8001/docs>

Terminal 2, dashboard:

```bash
python -m streamlit run dashboard/app.py
```

Dashboard: <http://localhost:8501>

El puerto de la API se puede cambiar con la variable de entorno `PORT`, y el dashboard y las pruebas la localizan con `API_URL`. Los valores por defecto son `8001` y `http://localhost:8001`.

Para regenerar el dataset y los graficos del analisis exploratorio:

```bash
python src/generate_dataset.py
python src/eda.py
```

Para reentrenar el modelo:

```bash
python src/train.py
```

Cualquier cambio en el codificado de variables o en el dataset invalida `models/model.pkl` y obliga a reentrenar y a actualizar las metricas de este README y del manual.

## API

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| GET | `/` | Mensaje de bienvenida |
| GET | `/health` | Estado del servicio y si el modelo cargo |
| GET | `/features` | Variables esperadas y valores categoricos admitidos |
| POST | `/predict` | Prediccion de precio a partir de las 12 caracteristicas |
| POST | `/run-eda` | Ejecuta el analisis exploratorio y devuelve su salida |

Ejemplo de request:

```bash
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "area": 7500,
    "bedrooms": 4,
    "bathrooms": 2,
    "stories": 3,
    "mainroad": "yes",
    "guestroom": "no",
    "basement": "no",
    "hotwaterheating": "no",
    "airconditioning": "yes",
    "parking": 2,
    "prefarea": "yes",
    "furnishingstatus": "furnished"
  }'
```

Respuesta:

```json
{
  "predicted_price": 7544529.02,
  "currency": "INR",
  "features": { "area": 7500, "...": "..." }
}
```

La prediccion se construye con `get_dummies` sobre una fila y luego se completan con cero las columnas ausentes segun `model.feature_names_in_`, que fijan el orden esperado por el modelo. Es lo que permite enviar una categoria distinta a las vistas en el entrenamiento sin romper la alineacion.

## Modelo

Random Forest Regressor de scikit-learn, con la siguiente configuracion:

| Parametro | Valor | Motivo |
| --- | --- | --- |
| `n_estimators` | 100 | Arboles que componen el ensamble |
| `n_jobs` | -1 | Usa todos los nucleos disponibles |
| `random_state` | 42 | Reproducibilidad del entrenamiento |

Se eligio Random Forest porque captura relaciones no lineales entre superficie, servicios y amenidades, tolera bien el sobreajuste con este volumen de datos y no requiere ajuste de hiperparametros para obtener un resultado utilizable. No se aplica escalado de variables: los arboles parten por umbrales y el escalado no modifica sus decisiones.

El preprocesamiento es deliberadamente simple: carga del CSV, codificacion one-hot con `drop_first=True` para las siete variables categoricas y division 80/20 con `random_state=42`.

## Resultados

Sobre el conjunto de prueba (200 registros del total de 1000):

| Metrica | Valor |
| --- | --- |
| MAE | 948,269.85 |
| R2 | 0.8301 |

El MAE indica que la prediccion se desvía en promedio cerca de un 14% del precio medio de la muestra (7.089.169,28). El R2 indica que el modelo explica aproximadamente el 83% de la varianza del precio.

Los precios estan en rupias, porque el dataset sigue la distribucion de un conjunto publico de viviendas de India. Los datos son sinteticos y se generan con `src/generate_dataset.py` de forma reproducible (semilla 42).

Escenarios de validacion definidos en el manual:

| Escenario | Caracteristicas | Prediccion |
| --- | --- | --- |
| Casa de lujo | 10.000 sq. ft, 4 dormitorios, todos los amenities | 10.609.837,43 |
| Casa economica | 3.000 sq. ft, 2 dormitorios, sin amenities | 3.242.018,99 |

## Pruebas

16 pruebas automatizadas con Pytest: 13 corren sin servicios levantados y 3 (`tests/test_api.py`) verifican el contrato contra la API en `localhost:8001`, por lo que requieren la API arriba.

```bash
# Suite completa (con la API corriendo en otra terminal)
python -m pytest tests/ -v

# Solo las que no necesitan servicios
python -m pytest tests/ --ignore=tests/test_api.py -q

# Cobertura
python -m pytest tests/ --cov=src --cov-report=term-missing
```

Cobertura actual: 36% de `src/`, con 74% en `app.py` y 71% en `predict.py`. `eda.py`, `train.py` y `generate_dataset.py` quedan en 0% porque se ejecutan como scripts y las pruebas no los importan.

## Estructura del proyecto

```
dashboard/       Interfaz Streamlit; consume la API
data/            Dataset generado (Housing.csv)
docs/            Manual de usuario, graficos y evidencias
models/          Modelo entrenado (model.pkl)
notebooks/       Notebook del analisis exploratorio
src/             Codigo fuente
  app.py             API FastAPI
  train.py           Entrenamiento del modelo
  predict.py         Prediccion por linea de comandos
  eda.py             Analisis exploratorio
  generate_dataset.py Generacion del dataset
tests/           Pruebas automatizadas
requirements.txt Dependencias
```

## Documentacion adicional

- [Manual de usuario](docs/pruebas/MANUAL_USUARIO.md): instalacion paso a paso, escenarios de validacion y checklist de entrega.
- `docs/pruebas/evidencias/`: capturas del dashboard con los dos escenarios y la salida del analisis exploratorio.
- `notebooks/EDA.ipynb`: analisis exploratorio interactivo.