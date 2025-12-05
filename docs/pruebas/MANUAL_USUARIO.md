# 📘 Manual de Usuario y Guía de Operaciones
## Sistema de Predicción de Precios de Viviendas

### 1. Introducción
Este documento sirve como guía oficial para la instalación, despliegue y validación del sistema de Machine Learning diseñado para la predicción de precios inmobiliarios. [cite_start]El sistema permite realizar análisis exploratorios, entrenar modelos predictivos y servir predicciones mediante una API y un Dashboard interactivo[cite: 3].

### 2. Instalación y Configuración Inicial

**Requisitos Previos:**
* Python 3.8 o superior.
* Git instalado.
* Terminal (PowerShell, Git Bash o CMD).

**Pasos de Instalación:**

1.  **Clonar el repositorio:**
    Abre tu terminal en la carpeta donde deseas guardar el proyecto:
    ```bash
    git clone [https://github.com/Bhalde2/trabajo_mineria.git](https://github.com/Bhalde2/trabajo_mineria.git)
    cd trabajo_mineria
    ```

2.  **Instalar dependencias:**
    [cite_start]Instala todas las librerías necesarias listadas en `requirements.txt`[cite: 5]:
    ```bash
    pip install -r requirements.txt
    ```

---

### 3. Módulos del Sistema (Flujo de Trabajo)

El proyecto se compone de 4 módulos principales. Se recomienda ejecutarlos en este orden:

#### A. Generación de Datos y EDA (Análisis Exploratorio)
[cite_start]Este paso crea el dataset base y genera los gráficos estadísticos en la carpeta `docs/pruebas/`[cite: 6, 10].

* **Opción 1: Comando Manual**
    ```bash
    python src/generate_dataset.py
    python src/eda.py
    ```

* **Opción 2: Desde el Dashboard**
    Una vez iniciado el Dashboard, puedes usar el botón **"🔄 Ejecutar Nuevo Análisis (EDA)"** en la barra lateral para regenerar los gráficos automáticamente.

#### B. Entrenamiento del Modelo
[cite_start]Entrena el algoritmo (Random Forest) con los datos procesados[cite: 14].

* **Comando:**
    ```bash
    python src/train.py
    ```

* **Métricas de Desempeño Esperadas:**
    [cite_start]El sistema debería reportar métricas cercanas a[cite: 19, 20]:
    * **MAE (Error Absoluto Medio):** ~1,021,546.04
    * **R2 Score:** ~0.61

#### C. Iniciar la API (Backend)
[cite_start]Levanta el servidor FastAPI que procesa las predicciones[cite: 21, 23].

* **Comando (Terminal 1):**
    ```bash
    python src/app.py
    ```
* [cite_start]**URL de Documentación:** `http://localhost:8001/docs` [cite: 24]
* **Endpoints Clave:**
    * [cite_start]`GET /health`: Verifica el estado del servicio[cite: 29].
    * [cite_start]`POST /predict`: Realiza predicciones de precios[cite: 31].

#### D. Iniciar el Dashboard (Frontend)
[cite_start]Lanza la interfaz gráfica Streamlit para el usuario final[cite: 32, 34].

* **Comando (Terminal 2):**
    ```bash
    python -m streamlit run dashboard/app.py
    ```
* [cite_start]**URL de Acceso:** `http://localhost:8501` [cite: 35]

---

### 4. Escenarios de Validación (Demo)

[cite_start]Para verificar la lógica del modelo, utilice los siguientes escenarios de prueba en el Dashboard[cite: 53, 68].

#### 🏠 Escenario 1: Casa de Lujo (High-End)
[cite_start]Configure los controles con los siguientes valores [cite: 54-66]:

| Parámetro | Valor a Seleccionar |
| :--- | :--- |
| **Área** | 10,000 |
| **Habitaciones** | 4 |
| **Baños** | 3 |
| **Pisos** | 3 |
| **Estacionamiento** | 2 |
| **Extras** | **SÍ** a todo (Carretera, Invitados, Sótano, Calentador, AC, Área Pref.) |
| **Amueblado** | Furnished (Amueblado) |

* [cite_start]**💰 Predicción Esperada:** Entre **₹6,000,000 y ₹8,000,000**[cite: 67].

#### 🏠 Escenario 2: Casa Económica (Budget)
[cite_start]Configure los controles con los siguientes valores [cite: 69-81]:

| Parámetro | Valor a Seleccionar |
| :--- | :--- |
| **Área** | 3,000 |
| **Habitaciones** | 2 |
| **Baños** | 1 |
| **Pisos** | 1 |
| **Estacionamiento** | 0 |
| **Extras** | **NO** a todo |
| **Amueblado** | Unfurnished (Sin amueblar) |

* [cite_start]**💰 Predicción Esperada:** Entre **₹2,000,000 y ₹4,000,000**[cite: 82].

---

### 5. Verificación Técnica (QA)

[cite_start]Para garantizar la integridad del código, ejecute la suite de tests unitarios[cite: 40].

* **Comando:**
    ```bash
    python -m pytest tests/ -v
    ```
    [cite_start]*(Nota: Asegúrese de respetar los espacios en el comando)*[cite: 42].

* **Resultado Requerido:**
    [cite_start]La consola debe mostrar **8 passed** (8 pruebas pasadas exitosamente) en color verde[cite: 45, 100].

---

### 6. Checklist de Entrega

[cite_start]Verifique los siguientes puntos antes de finalizar[cite: 96]:

- [ ] [cite_start]API FastAPI funcionando en puerto 8001[cite: 97].
- [ ] [cite_start]Dashboard Streamlit funcionando en puerto 8501[cite: 98].
- [ ] [cite_start]Modelo entrenado con MAE ~1.02M[cite: 99].
- [ ] [cite_start]Tests unitarios 8/8 pasando[cite: 100].
- [ ] [cite_start]EDA completado con gráficos en carpeta `docs`[cite: 101].
- [ ] [cite_start]Evidencias visuales capturadas (Screenshots/Video)[cite: 104].
