import streamlit as st
import pandas as pd
import joblib
import os
import sys

# Agregar src al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Título
st.set_page_config(
    page_title="Housing Price Predictor",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Housing Price Prediction")
st.markdown("Predice el precio de viviendas basado en sus características")

# Función para cargar modelo
def load_trained_model():
    """Cargar modelo entrenado"""
    try:
        model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'model.pkl')
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"Error cargando modelo: {e}")
        return None

# Función para predecir
def predict_price(model, input_data):
    """Realizar predicción con el modelo"""
    try:
        # Convertir input a DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Encoding igual que en entrenamiento
        input_encoded = pd.get_dummies(input_df, drop_first=True)
        
        # Asegurar mismas columnas que entrenamiento
        if hasattr(model, 'feature_names_in_'):
            for col in model.feature_names_in_:
                if col not in input_encoded.columns:
                    input_encoded[col] = 0
            input_encoded = input_encoded[model.feature_names_in_]
        
        # Realizar predicción
        prediction = model.predict(input_encoded)
        return prediction[0]
    
    except Exception as e:
        raise Exception(f"Error en predicción: {str(e)}")

# Sidebar para entrada de datos
st.sidebar.header("Características de la Vivienda")

# Inputs numéricos
area = st.sidebar.number_input("Área (sq. ft)", min_value=500, max_value=20000, value=7500)
bedrooms = st.sidebar.slider("Habitaciones", min_value=1, max_value=6, value=3)
bathrooms = st.sidebar.slider("Baños", min_value=1, max_value=4, value=2)
stories = st.sidebar.slider("Pisos", min_value=1, max_value=4, value=2)
parking = st.sidebar.slider("Plazas de parking", min_value=0, max_value=3, value=1)

# Inputs categóricos
mainroad = st.sidebar.selectbox("Carretera principal", ["yes", "no"])
guestroom = st.sidebar.selectbox("Cuarto de invitados", ["yes", "no"])
basement = st.sidebar.selectbox("Sótano", ["yes", "no"])
hotwaterheating = st.sidebar.selectbox("Calentador agua", ["yes", "no"])
airconditioning = st.sidebar.selectbox("Aire acondicionado", ["yes", "no"])
prefarea = st.sidebar.selectbox("Área preferencial", ["yes", "no"])
furnishingstatus = st.sidebar.selectbox("Amueblado", ["furnished", "semi-furnished", "unfurnished"])

# Botón de predicción
if st.sidebar.button("🎯 Predecir Precio", type="primary"):
    # Preparar datos
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
    
    # Cargar modelo y predecir
    model = load_trained_model()
    if model is not None:
        try:
            predicted_price = predict_price(model, input_data)
            
            # Mostrar resultado
            st.success(f"### 💰 Precio Predicho: ₹{predicted_price:,.2f}")
            
            # Mostrar detalles
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
            st.error(f"❌ Error en la predicción: {str(e)}")
    else:
        st.error("❌ No se pudo cargar el modelo. Ejecuta train.py primero.")

# Información adicional
st.markdown("---")
st.subheader("📊 Información del Modelo")
st.markdown("""
- **Algoritmo**: Random Forest Regressor
- **Precisión**: MAE ~₹1,021,546
- **R² Score**: 0.61
- **Dataset**: 545 propiedades residenciales
- **Características**: 12 variables predictoras
""")

# Ejemplo de API
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