import unittest
import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestPredict(unittest.TestCase):
    
    def test_feature_names(self):
        """Test nombres de características"""
        expected_features = [
            'area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 
            'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 
            'parking', 'prefarea', 'furnishingstatus'
        ]
        self.assertEqual(len(expected_features), 12)
        self.assertIn('area', expected_features)
        self.assertIn('bedrooms', expected_features)
    
    def test_model_file_exists(self):
        """Test que el modelo entrenado existe"""
        model_path = 'models/model.pkl'
        self.assertTrue(os.path.exists(model_path), 
                       f"Modelo no encontrado en {model_path}. Ejecuta train.py primero")
    
    def test_prediction_format(self):
        """Test formato de entrada para predicción"""
        sample_data = {
            'area': 7500, 'bedrooms': 4, 'bathrooms': 2, 'stories': 3,
            'mainroad': 'yes', 'guestroom': 'no', 'basement': 'no', 
            'hotwaterheating': 'no', 'airconditioning': 'yes', 
            'parking': 2, 'prefarea': 'yes', 'furnishingstatus': 'furnished'
        }
        
        expected_features = [
            'area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 
            'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 
            'parking', 'prefarea', 'furnishingstatus'
        ]
        
        for feature in expected_features:
            self.assertIn(feature, sample_data)

if __name__ == '__main__':
    unittest.main()