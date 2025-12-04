# Housing Price Prediction - Proyecto de Machine Learning

## 📋 Descripción
Sistema completo para **predecir precios de viviendas** utilizando Machine Learning, una **API REST** creada con FastAPI y un **dashboard interactivo** construido con Streamlit.  
El proyecto incluye análisis exploratorio (EDA), preprocesamiento, entrenamiento, pruebas y despliegue de un modelo de regresión.

---

## 🎯 2. Problema a Resolver

Los precios de viviendas suelen ser difíciles de estimar debido a:

- Variaciones de mercado  
- Diferencias en ubicación  
- Características estructurales diversas  
- Subjetividad en la valoración humana  

Esto puede generar:

- Tasaciones inexactas  
- Pérdida de oportunidades de inversión  
- Decisiones mal informadas por parte de compradores o vendedores

---
## 🛠️ Solución
Para resolver el problema, se implementó un sistema automatizado basado en Machine Learning, compuesto por:
- **Modelo**: Random Forest Regressor
- **API**: FastAPI para predicciones en tiempo real
- **Dashboard**: Streamlit para interfaz de usuario
- **Métricas**: MAE ~₹500,000, R² ~0.85

## 🧹 Preprocesamiento de Datos

El preprocesamiento es una etapa fundamental del proyecto, ya que permite preparar los datos correctamente antes de entrenar el modelo de Machine Learning. En este proyecto se utilizan las librerías pandas y numpy para el tratamiento de los datos.

Las principales tareas realizadas en esta etapa son:

✅ Carga de datos

Se cargan los datos desde el dataset de viviendas, donde cada registro representa una propiedad con diferentes atributos como:

Superficie

Número de habitaciones

Presencia de estacionamiento

Ubicación

Servicios adicionales, entre otros.

✅ Limpieza de datos

Se realiza una depuración del dataset para:

Eliminar valores nulos.

Corregir datos inconsistentes.

Asegurar que cada variable tenga el tipo de dato correcto.

Esto evita errores durante el entrenamiento y mejora la calidad de las predicciones.

✅ Transformación de variables categóricas

Las variables categóricas (por ejemplo, si la vivienda tiene estacionamiento o no) son transformadas a valores numéricos mediante One-Hot Encoding, permitiendo que el modelo las interprete correctamente.

✅ Separación de los datos

Finalmente, los datos se dividen en:

Variables de entrada (X)

Variable objetivo (y) → Precio de la vivienda

Y posteriormente se separan en:

Conjunto de entrenamiento

Conjunto de prueba

Esto permite evaluar el rendimiento real del modelo.

## 🌲 Análisis del Modelo

El algoritmo utilizado es Random Forest Regressor, implementado con la librería scikit-learn.

🔍 Descripción del modelo

Random Forest es un modelo compuesto por múltiples árboles de decisión que trabajan de forma conjunta. Cada árbol genera una predicción y el resultado final corresponde al promedio de todas ellas.

⚙️ Parámetros principales del modelo

El modelo se configuró con los siguientes parámetros:

n_estimators = 100 → Se utilizan 100 árboles de decisión.

n_jobs = -1 → Se emplean todos los núcleos del procesador disponibles.

random_state = 42 → Permite que los resultados sean reproducibles.

✅ Justificación del uso de Random Forest

Este modelo fue elegido debido a que:

Maneja correctamente relaciones no lineales.

Es robusto frente al sobreajuste (overfitting).

Permite trabajar con datos numéricos y categóricos.

Entrega buenas predicciones sin necesidad de ajustes complejos.

En este proyecto se obtuvo un coeficiente R² cercano a 0.85, lo cual indica un alto nivel de precisión.

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

💾 Guardado del modelo

Una vez entrenado, el modelo se guarda utilizando la librería joblib en la carpeta models/, lo que permite su reutilización en:

La API REST desarrollada con FastAPI.

El dashboard interactivo desarrollado con Streamlit.
