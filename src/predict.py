import pandas as pd
import joblib
import sys
import os

def load_trained_model(model_path=None):
    """Cargar modelo entrenado"""
    try:
        # Anclado al archivo: la ruta relativa depended de dónde se ejecute.
        model_path = model_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'model.pkl')
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        raise Exception("Modelo no encontrado. Ejecuta train.py primero.")

def predict_price(model, input_data):
    """Realizar predicción con el modelo"""
    try:
        # Convertir input a DataFrameS
        if isinstance(input_data, dict):
            input_df = pd.DataFrame([input_data])
        else:
            input_df = input_data

        # El modelo se entrenó con get_dummies: hay que replicar el encoding y su orden
        input_encoded = pd.get_dummies(input_df, drop_first=True)
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

def get_feature_names():
    """Obtener nombres de características esperadas"""
    return ['area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 
            'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 
            'parking', 'prefarea', 'furnishingstatus']

if __name__ == "__main__":
    # Solo al ejecutarlo directo: en consola cp1252 los emojis rompen el print.
    sys.stdout.reconfigure(encoding="utf-8")

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

