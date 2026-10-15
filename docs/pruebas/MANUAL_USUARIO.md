# 📘 Manual de Usuario y Guía de Operaciones
## Sistema de Predicción de Precios de Viviendas

### 1. Introducción
Este documento sirve como guía oficial para la instalación, despliegue y validación del sistema de Machine Learning diseñado para la predicción de precios inmobiliarios. El sistema permite realizar análisis exploratorios, entrenar modelos predictivos y servir predicciones mediante una API y un Dashboard interactivo.

### 2. Instalación y Configuración Inicial

**Requisitos Previos:**
* Python 3.8 o superior.
* Git instalado.
* Terminal (PowerShell, Git Bash o CMD).

**Pasos de Instalación:**

1.  **Clonar el repositorio:**
    Abre tu terminal en la carpeta donde deseas guardar el proyecto:
    ```bash
    git clone https://github.com/Bhalde2/trabajo_mineria.git
    cd trabajo_mineria
    ```

2.  **Instalar dependencias:**
    Instala todas las librerías necesarias listadas en `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

---

### 3. Módulos del Sistema (Flujo de Trabajo)

El proyecto se compone de 4 módulos principales. Se recomienda ejecutarlos en este orden:

#### A. Generación de Datos y EDA (Análisis Exploratorio)
Este paso crea el dataset base y genera los gráficos estadísticos en la carpeta `docs/pruebas/`.

* **Opción 1: Comando Manual**
    ```bash
    python src/generate_dataset.py
    python src/eda.py
    ```

* **Opción 2: Desde el Dashboard**
    Una vez iniciado el Dashboard, puedes usar el botón **"📊 Ejecutar Análisis Exploratorio de Datos (EDA)"** al final de la página para regenerar los gráficos automáticamente.

#### B. Entrenamiento del Modelo
Entrena el algoritmo (Random Forest) con los datos procesados.

* **Comando:**
    ```bash
    python src/train.py
    ```

* **Métricas de Desempeño Esperadas:**
    El sistema debería reportar métricas cercanas a:
    * **MAE (Error Absoluto Medio):** ~948,270
    * **R2 Score:** ~0.83

#### C. Iniciar la API (Backend)
Levanta el servidor FastAPI que procesa las predicciones.

* **Comando (Terminal 1):**
    ```bash
    python src/app.py
    ```
* **URL de Documentación:** `http://localhost:8001/docs`
* **Endpoints Clave:**
    * `GET /health`: Verifica el estado del servicio.
    * `POST /predict`: Realiza predicciones de precios.
    * `POST /run-eda`: Ejecuta el análisis exploratorio de datos.

#### D. Iniciar el Dashboard (Frontend)
Lanza la interfaz gráfica Streamlit para el usuario final.

* **Comando (Terminal 2):**
    ```bash
    python -m streamlit run dashboard/app.py
    ```
* **URL de Acceso:** `http://localhost:8501`

---

### 4. Escenarios de Validación (Demo)

Para verificar la lógica del modelo, utilice los siguientes escenarios de prueba en el Dashboard.

#### 🏠 Escenario 1: Casa de Lujo (High-End)
Configure los controles con los siguientes valores:

| Parámetro | Valor a Seleccionar |
| :--- | :--- |
| **Área** | 10,000 |
| **Habitaciones** | 4 |
| **Baños** | 3 |
| **Pisos** | 3 |
| **Estacionamiento** | 2 |
| **Extras** | **SÍ** a todo (Carretera, Invitados, Sótano, Calentador, AC, Área Pref.) |
| **Amueblado** | Furnished (Amueblado) |

* **💰 Predicción Esperada:** Entre **₹9,000,000 y ₹12,000,000** (valor real con el modelo actual: ~₹10,600,000).

#### 🏠 Escenario 2: Casa Económica (Budget)
Configure los controles con los siguientes valores:

| Parámetro | Valor a Seleccionar |
| :--- | :--- |
| **Área** | 3,000 |
| **Habitaciones** | 2 |
| **Baños** | 1 |
| **Pisos** | 1 |
| **Estacionamiento** | 0 |
| **Extras** | **NO** a todo |
| **Amueblado** | Unfurnished (Sin amueblar) |

* **💰 Predicción Esperada:** Entre **₹2,000,000 y ₹4,000,000** (valor real con el modelo actual: ~₹3,240,000).

---

### 5. Verificación Técnica (QA)

Para garantizar la integridad del código, ejecute la suite de tests unitarios.

* **Comando:**
    ```bash
    python -m pytest tests/ -v
    ```
    *(Nota: los 3 tests de `tests/test_api.py` requieren la API corriendo en el puerto 8001; sin ella fallan por `ConnectionError`)*.

* **Resultado Requerido:**
    La consola debe mostrar **16 passed** (16 pruebas pasadas exitosamente) en color verde.

* **Cobertura:**
    ```bash
    python -m pytest tests/ --cov=src --cov-report=term-missing
    ```
    Cobertura actual: **36%** de `src/` (74% en `app.py`, 71% en `predict.py`).

---

### 6. Checklist de Entrega

Verifique los siguientes puntos antes de finalizar:

- [ ] API FastAPI funcionando en puerto 8001.
- [ ] Dashboard Streamlit funcionando en puerto 8501.
- [ ] Modelo entrenado con MAE ~₹948,270 y R² ~0.83.
- [x] Tests unitarios 16/16 pasando (36% de cobertura sobre `src/`).
- [ ] EDA completado con gráficos en carpeta `docs/pruebas`.
- [x] Evidencias visuales capturadas en `docs/pruebas/evidencias/` (escenarios 1 y 2 + salida del EDA).