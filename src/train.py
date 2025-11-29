import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

def main():
    print("🏋️ Entrenando modelo...")
    
    # Cargar datos directamente
    df = pd.read_csv('data/Housing.csv')
    print(f"✅ Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
    
    X = df.drop('price', axis=1)
    y = df['price']
    
    # Encoding básico (sin preprocess.py)
    X_encoded = pd.get_dummies(X, drop_first=True)
    print(f"✅ Features después de encoding: {X_encoded.shape[1]} columnas")
    
    # Dividir datos
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42
    )
    print(f"✅ Datos divididos: Train {X_train.shape[0]}, Test {X_test.shape[0]}")
    
    # Entrenar modelo
    print("⏳ Entrenando Random Forest...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Evaluar
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"✅ Modelo entrenado!")
    print(f"📊 MAE: ₹{mae:,.2f}")
    print(f"📈 R²: {r2:.4f}")
    
    # Guardar modelo
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/model.pkl')
    print("💾 Modelo guardado en models/model.pkl")

if __name__ == "__main__":
    main()