# 🏡 Housing Price Prediction - Proyecto de Machine Learning

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.2-red)
![Status](https://img.shields.io/badge/Status-Terminado-success)

> **Sistema inteligente para la valoración inmobiliaria basado en Machine Learning.**

---

## 📚 Documentación
Para ver la guía detallada de uso, escenarios de prueba y explicación paso a paso, consulta:

### [📘 CLIC AQUÍ PARA VER EL MANUAL DE USUARIO](/docs/pruebas/MANUAL_USUARIO.md)


---

## 📋 Descripción
Este proyecto implementa un flujo completo de **MLOps** para predecir precios de viviendas. Integra un modelo de regresión entrenado, servido a través de una **API REST** de alto rendimiento (FastAPI) y consumido por una interfaz amigable (**Dashboard**) construida en Streamlit.

El sistema abarca desde el análisis exploratorio de datos (EDA) hasta el despliegue del modelo.

## 🎯 Problema y Solución

| ⚠️ El Problema | ✅ La Solución |
| :--- | :--- |
| Tasaciones subjetivas e inexactas. | **Modelo Random Forest** robusto y objetivo. |
| Variabilidad del mercado difícil de rastrear. | **API en tiempo real** para consultas instantáneas. |
| Pérdida de oportunidades de inversión. | **Dashboard interactivo** para simulación de escenarios. |

---

## 🚀 Inicio Rápido

Si deseas ejecutar este proyecto en tu máquina local:

### 1. Instalación

```
# Clonar repositorio
git clone [https://github.com/Bhalde2/trabajo_mineria.git](https://github.com/Bhalde2/trabajo_mineria.git)
cd trabajo_mineria

# Instalar dependencias
pip install -r requirements.txt

```

### 2. Ejecución
Puedes levantar los servicios en terminales separadas:

## Terminal 1 (API):

python src/app.py
# Disponible en: http://localhost:8001/docs

## Terminal 2 (Dashboard):

python -m streamlit run dashboard/app.py
# Disponible en: http://localhost:8501

## 🧪 Tests
8 tests unitarios con Pytest. 5 corren sin servicios levantados; los 3 de `tests/test_api.py` necesitan la API viva en el puerto 8001.

```bash
# Con la API corriendo en otra terminal:
python -m pytest tests/ -v
```

## 🧹 Preprocesamiento de Datos (Pipeline)
El pipeline de datos utiliza pandas y numpy para asegurar la calidad de la información antes del entrenamiento:

📥 Carga e Ingesta: Lectura del dataset crudo con atributos de superficie, habitaciones y servicios.

🧼 Limpieza: Imputación de valores nulos y corrección de inconsistencias.

🔢 Transformación: Aplicación de One-Hot Encoding para variables categóricas (ej. Aire Acondicionado: Sí/No).

✂️ Split de Datos: División estratégica en conjuntos de entrenamiento (Train) y validación (Test).

## 🌲 Análisis del Modelo

El algoritmo utilizado es Random Forest Regressor, implementado con la librería scikit-learn.

## 🔍 Descripción del modelo

Random Forest es un modelo compuesto por múltiples árboles de decisión que trabajan de forma conjunta. Cada árbol genera una predicción y el resultado final corresponde al promedio de todas ellas.

## ⚙️ Parámetros principales del modelo

El modelo se configuró con los siguientes parámetros:

n_estimators = 100 → Se utilizan 100 árboles de decisión.

n_jobs = -1 → Se emplean todos los núcleos del procesador disponibles.

random_state = 42 → Permite que los resultados sean reproducibles.

## ✅ Justificación del uso de Random Forest

Este modelo fue elegido debido a que:

Maneja correctamente relaciones no lineales.

Es robusto frente al sobreajuste (overfitting).

Permite trabajar con datos numéricos y categóricos.

Entrega buenas predicciones sin necesidad de ajustes complejos.

En este proyecto se obtuvo un R² de ~0.83, lo cual indica un alto nivel de precisión.

## 🏋️ Entrenamiento del Modelo

El entrenamiento del modelo se realiza en el archivo src/train.py y sigue las siguientes etapas:

1. Carga de los datos preprocesados.

2. Separación en conjuntos de entrenamiento y prueba.

3. Inicialización del modelo Random Forest.

4. Entrenamiento mediante el método fit().

5. Evaluación del rendimiento mediante predicciones sobre el conjunto de prueba.

📏 Evaluación del rendimiento

El modelo es evaluado utilizando las siguientes métricas:

MAE (Mean Absolute Error – Error Absoluto Medio):
Indica el error promedio entre el valor real y el valor predicho.

R² (Coeficiente de Determinación):
Mide qué tan bien el modelo explica el comportamiento de los precios.

## 💾 Guardado del modelo

Una vez entrenado, el modelo se guarda utilizando la librería joblib en la carpeta models/, lo que permite su reutilización en:

La API REST desarrollada con FastAPI.

El dashboard interactivo desarrollado con Streamlit.

## 📂 Estructura del Proyecto

├── dashboard/       # Código de la interfaz Streamlit
├── data/            # Dataset generado (Housing.csv)
├── docs/            # Documentación y Manual de Usuario
├── models/          # Modelos entrenados (.pkl/.joblib)
├── notebooks/       # Notebook de EDA
├── src/             # Código fuente (API, Entrenamiento, EDA)
├── tests/           # Tests unitarios con Pytest
├── requirements.txt # Dependencias del proyecto
└── README.md        # Este archivo
