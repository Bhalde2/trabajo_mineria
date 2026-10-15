from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
import joblib
import pandas as pd
import os
import subprocess
import sys

# La consola de Windows usa cp1252 y revienta con los emojis; los prints van en utf-8.
sys.stdout.reconfigure(encoding="utf-8")

PORT = int(os.environ.get("PORT", 8001))

app = FastAPI(
    title="Housing Price Prediction API",
    description="API para predecir precios de viviendas",
    version="1.0.0"
)

# ============================
#  CARGA DE MODELO
# ============================
try:
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'model.pkl')
    model_path = os.path.abspath(model_path)

    print(f"🔍 Intentando cargar modelo desde: {model_path}")

    model = joblib.load(model_path)
    print("✅ Modelo cargado exitosamente")

except Exception as e:
    print(f"❌ Error cargando modelo: {e}")
    model = None


# ============================
#  SCHEMA DE FEATURES
# ============================
class HouseFeatures(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
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
    })

    area: int
    bedrooms: int
    bathrooms: int
    stories: int
    mainroad: str
    guestroom: str
    basement: str
    hotwaterheating: str
    airconditioning: str
    parking: int
    prefarea: str
    furnishingstatus: str


# ============================
#   ENDPOINTS BÁSICOS
# ============================
@app.get("/")
def read_root():
    return {"message": "Housing Price Prediction API - Usa /docs para documentación"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}


@app.get("/features")
def get_features_info():
    return {
        "expected_features": [
            'area', 'bedrooms', 'bathrooms', 'stories', 'mainroad',
            'guestroom', 'basement', 'hotwaterheating', 'airconditioning',
            'parking', 'prefarea', 'furnishingstatus'
        ],
        "categorical_values": {
            "mainroad": ["yes", "no"],
            "guestroom": ["yes", "no"],
            "basement": ["yes", "no"],
            "hotwaterheating": ["yes", "no"],
            "airconditioning": ["yes", "no"],
            "prefarea": ["yes", "no"],
            "furnishingstatus": ["furnished", "semi-furnished", "unfurnished"]
        }
    }


# ============================
#   ENDPOINT DE PREDICCIÓN
# ============================
@app.post("/predict")
def predict(features: HouseFeatures):
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no disponible")

    try:
        input_data = features.model_dump()
        input_df = pd.DataFrame([input_data])
        input_encoded = pd.get_dummies(input_df, drop_first=True)

        # Asegurar columnas correctas
        if hasattr(model, 'feature_names_in_'):
            for col in model.feature_names_in_:
                if col not in input_encoded.columns:
                    input_encoded[col] = 0
            input_encoded = input_encoded[model.feature_names_in_]

        predicted_price = model.predict(input_encoded)[0]

        return {
            "predicted_price": round(predicted_price, 2),
            "currency": "INR",
            "features": input_data
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en predicción: {str(e)}")


# ============================
#   ENDPOINT PARA EJECUTAR EDA
# ============================
@app.post("/run-eda")
def run_eda():
    try:
        # El archivo real es src/eda.py en minúsculas; en Linux el nombre importa.
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "eda.py"))

        print(f"▶ Ejecutando eda.py desde: {script_path}")

        if not os.path.isfile(script_path):
            raise FileNotFoundError(f"eda.py no encontrado en: {script_path}")

        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            # Sin esto el hijo imprime en cp1252 y los acentos llegan corruptos al dashboard.
            env={**os.environ, "PYTHONIOENCODING": "utf-8"}
        )

        return {
            "status": "ok",
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================
#   EJECUCIÓN DIRECTA
# ============================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)