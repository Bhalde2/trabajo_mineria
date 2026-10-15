import unittest
import os
import sys

from fastapi.testclient import TestClient

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app

client = TestClient(app)

SAMPLE = {
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


class TestAppInProcess(unittest.TestCase):
    """Prueba la API sin levantar uvicorn, para que la cobertura vea src/app.py"""

    def test_health(self):
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["model_loaded"])

    def test_predict(self):
        response = client.post("/predict", json=SAMPLE)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertGreater(body["predicted_price"], 1_000_000)
        self.assertLess(body["predicted_price"], 20_000_000)
        self.assertEqual(body["currency"], "INR")

    def test_predict_rejects_incomplete_payload(self):
        response = client.post("/predict", json={"area": 7500})
        self.assertEqual(response.status_code, 422)

    def test_health_matches_live_api_result(self):
        # La ruta in-process y la API por HTTP deben dar el mismo precio.
        in_process = client.post("/predict", json=SAMPLE).json()["predicted_price"]
        try:
            import requests
            live = requests.post(
                os.environ.get("API_URL", "http://localhost:8001") + "/predict",
                json=SAMPLE, timeout=10
            ).json()["predicted_price"]
        except Exception:
            self.skipTest("API no levantada en localhost:8001")
        self.assertAlmostEqual(in_process, live, delta=0.01)


if __name__ == '__main__':
    unittest.main()