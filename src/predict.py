import pandas as pd
import joblib
from preprocess import load_data

def load_trained_model(model_path='../models/model.pkl'):
    """Cargar modelo entrenado"""
    try:
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        raise Exception("Modelo no encontrado. Ejecuta train.py primero.")

def predict_price(model, input_data):
    """Realizar predicción con el modelo"""
    try:
        # Convertir input a DataFrame
        if isinstance(input_data, dict):
            input_df = pd.DataFrame([input_data])
        else:
            input_df = input_data
        
        # Realizar predicción
        prediction = model.predict(input_df)
        return prediction[0]
    
    except Exception as e:
        raise Exception(f"Error en predicción: {str(e)}")

def get_feature_names():
    """Obtener nombres de características esperadas"""
    return ['area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 
            'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 
            'parking', 'prefarea', 'furnishingstatus']

if __name__ == "__main__":
    # Ejemplo de uso
    model = load_trained_model()
    sample_data = {
        'area': 7500, 'bedrooms': 4, 'bathrooms': 2, 'stories': 3,
        'mainroad': 'yes', 'guestroom': 'no', 'basement': 'no', 
        'hotwaterheating': 'no', 'airconditioning': 'yes', 
        'parking': 2, 'prefarea': 'yes', 'furnishingstatus': 'furnished'
    }
    
    price = predict_price(model, sample_data)
    print(f"💰 Precio predicho: ₹{price:,.2f}")