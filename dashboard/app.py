import streamlit as st
import pandas as pd
import joblib
import os
import sys
import time
import requests

# Agregar src al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# =============================
# CONFIGURACIÓN DEL DASHBOARD
# =============================
st.set_page_config(
    page_title="Housing Price Predictor",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Housing Price Prediction")
st.markdown("Predice el precio de viviendas basado en sus características")

API_URL = "http://localhost:8001"


# =============================
# FUNCIÓN PARA CARGAR MODELO
# =============================
def load_trained_model():
    """Cargar modelo entrenado"""
    try:
        model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'model.pkl')
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"Error cargando modelo: {e}")
        return None


# =============================
# FUNCIÓN DE PREDICCIÓN
# =============================
def predict_price(model, input_data):
    """Realizar predicción con el modelo"""
    try:
        input_df = pd.DataFrame([input_data])
        input_encoded = pd.get_dummies(input_df, drop_first=True)

        if hasattr(model, 'feature_names_in_'):
            for col in model.feature_names_in_:
                if col not in input_encoded.columns:
                    input_encoded[col] = 0

            input_encoded = input_encoded[model.feature_names_in_]

        prediction = model.predict(input_encoded)
        return prediction[0]

    except Exception as e:
        raise Exception(f"Error en predicción: {str(e)}")


# =============================
# SIDEBAR - INPUT FEATURES
# =============================
st.sidebar.header("Características de la Vivienda")

area = st.sidebar.number_input("Área (sq. ft)", min_value=500, max_value=20000, value=7500)
bedrooms = st.sidebar.slider("Habitaciones", 1, 6, 3)
bathrooms = st.sidebar.slider("Baños", 1, 4, 2)
stories = st.sidebar.slider("Pisos", 1, 4, 2)
parking = st.sidebar.slider("Plazas de parking", 0, 3, 1)

mainroad = st.sidebar.selectbox("Carretera principal", ["yes", "no"])
guestroom = st.sidebar.selectbox("Cuarto de invitados", ["yes", "no"])
basement = st.sidebar.selectbox("Sótano", ["yes", "no"])
hotwaterheating = st.sidebar.selectbox("Calentador agua", ["yes", "no"])
airconditioning = st.sidebar.selectbox("Aire acondicionado", ["yes", "no"])
prefarea = st.sidebar.selectbox("Área preferencial", ["yes", "no"])
furnishingstatus = st.sidebar.selectbox("Amueblado", ["furnished", "semi-furnished", "unfurnished"])


# =============================
# BOTÓN DE PREDICCIÓN
# =============================
if st.sidebar.button("🎯 Predecir Precio", type="primary"):
    input_data = {
        'area': area,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'stories': stories,
        'mainroad': mainroad,
        'guestroom': guestroom,
        'basement': basement,
        'hotwaterheating': hotwaterheating,
        'airconditioning': airconditioning,
        'parking': parking,
        'prefarea': prefarea,
        'furnishingstatus': furnishingstatus
    }

    with st.spinner("🔄 Cargando modelo y prediciendo..."):
        time.sleep(1)
        model = load_trained_model()

        if model:
            try:
                predicted_price = predict_price(model, input_data)

                st.success(f"### 💰 Precio Predicho: ₹{predicted_price:,.2f}")

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Características Ingresadas")
                    st.json(input_data)

                with col2:
                    st.subheader("Análisis")
                    st.metric("Área", f"{area:,} sq. ft")
                    st.metric("Habitaciones", bedrooms)
                    st.metric("Baños", bathrooms)
                    st.metric("Pisos", stories)

            except Exception as e:
                st.error(f"❌ Error en la predicción: {e}")


# =============================
# BOTÓN PARA EJECUTAR EDA
# =============================
st.markdown("---")
st.subheader("📊 Ejecutar Análisis Exploratorio de Datos (EDA)")

if st.button("▶ Ejecutar EDA"):
    with st.spinner("Ejecutando EDA.py... por favor espera..."):
        try:
            response = requests.post(f"{API_URL}/run-eda")

            if response.status_code == 200:
                result = response.json()
                st.success("EDA ejecutado correctamente")

                st.write("### 📄 Output del script EDA.py")
                st.code(result["stdout"], language="bash")

                if result["stderr"]:
                    st.warning("### ⚠ Advertencias / Errores del script")
                    st.code(result["stderr"], language="bash")

            else:
                st.error(f"Error desde el API: {response.text}")

        except Exception as e:
            st.error(f"No se pudo conectar con la API: {e}")


# =============================
# INFORMACIÓN DEL MODELO
# =============================
st.markdown("---")
st.subheader("📚 Información del Modelo")
st.markdown("""
- **Algoritmo**: Random Forest Regressor  
- **Precisión**: MAE ~₹948,270  
- **R² Score**: 0.83  
- **Dataset**: 1000 propiedades residenciales  
- **Características**: 12 variables predictoras  
""")

# Ejemplo de uso de API
with st.expander("🔧 Ejemplo de uso de API"):
    st.code("""
import requests

url = "http://localhost:8001/predict"
data = {
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
}

response = requests.post(url, json=data)
print(response.json())
""", language="python")