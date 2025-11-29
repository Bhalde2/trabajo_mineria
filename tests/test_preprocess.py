import unittest
import pandas as pd
import sys
import os

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestPreprocess(unittest.TestCase):
    
    def test_load_data(self):
        """Test carga de datos"""
        # RUTA CORREGIDA desde la raíz del proyecto
        df = pd.read_csv('data/Housing.csv')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 545)
        self.assertEqual(df.shape[1], 13)
        self.assertIn('price', df.columns)
        self.assertIn('area', df.columns)
    
    def test_data_quality(self):
        """Test calidad de datos"""
        df = pd.read_csv('data/Housing.csv')
        
        # Verificar que no hay valores nulos
        self.assertFalse(df.isnull().any().any())
        
        # Verificar rangos razonables
        self.assertGreater(df['price'].min(), 0)
        self.assertGreater(df['area'].min(), 0)
        self.assertLessEqual(df['bedrooms'].max(), 6)
        self.assertLessEqual(df['bathrooms'].max(), 4)

if __name__ == '__main__':
    unittest.main()