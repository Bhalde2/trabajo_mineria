import unittest
import requests
import time

class TestAPI(unittest.TestCase):
    
    BASE_URL = "http://localhost:8001"  # PUERTO CORREGIDO
    
    def test_health_endpoint(self):
        """Test endpoint de salud"""
        response = requests.get(f"{self.BASE_URL}/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("status", data)
        self.assertIn("model_loaded", data)
        self.assertTrue(data["model_loaded"])
    
    def test_features_endpoint(self):
        """Test endpoint de características"""
        response = requests.get(f"{self.BASE_URL}/features")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("expected_features", data)
        self.assertIn("categorical_values", data)
        self.assertEqual(len(data["expected_features"]), 12)
    
    def test_predict_endpoint(self):
        """Test endpoint de predicción"""
        test_data = {
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
        
        response = requests.post(
            f"{self.BASE_URL}/predict",
            json=test_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("predicted_price", data)
        self.assertIn("currency", data)
        self.assertIn("features", data)
        # Verificar que el precio sea razonable
        self.assertGreater(data["predicted_price"], 1000000)
        self.assertLess(data["predicted_price"], 20000000)

if __name__ == '__main__':
    unittest.main()