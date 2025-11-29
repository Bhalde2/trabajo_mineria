import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

def load_data(filepath):
    """Cargar dataset desde CSV"""
    return pd.read_csv(filepath)

def create_preprocessor():
    """Crear pipeline de preprocesamiento"""
    numeric_features = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']
    categorical_features = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 
                          'airconditioning', 'prefarea', 'furnishingstatus']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), categorical_features)
        ])
    
    return preprocessor

def save_preprocessor(preprocessor, filepath):
    """Guardar preprocesador entrenado"""
    joblib.dump(preprocessor, filepath)

def load_preprocessor(filepath):
    """Cargar preprocesador entrenado"""
    return joblib.load(filepath)

if __name__ == "__main__":
    # Ejemplo de uso
    df = load_data('../data/Housing.csv')
    preprocessor = create_preprocessor()
    print("Preprocesador creado exitosamente")