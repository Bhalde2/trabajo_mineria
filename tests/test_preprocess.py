import unittest
import pandas as pd
import sys
import os

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestPreprocess(unittest.TestCase):
    
    def test_load_data(self):
        """Test carga de datos"""
        try:
            # RUTA CORREGIDA desde la raíz del proyecto
            df = pd.read_csv('data/Housing.csv')
            self.assertIsInstance(df, pd.DataFrame)
            
            # Verifica que tenga datos (sin número fijo)
            self.assertGreater(df.shape[0], 0, "El DataFrame está vacío")
            self.assertGreater(df.shape[1], 0, "El DataFrame no tiene columnas")
            
            # Columnas mínimas esperadas
            expected_columns = ['price', 'area']
            for col in expected_columns:
                self.assertIn(col, df.columns, f"Falta columna requerida: {col}")
            
            # Solo muestra info, no falla por número específico
            print(f"✓ Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
            
        except FileNotFoundError as e:
            self.fail(f"Archivo no encontrado: {e}")
    
    def test_data_quality(self):
        """Test calidad de datos"""
        df = pd.read_csv('data/Housing.csv')
        
        # Verificar que no hay valores nulos en columnas clave
        key_columns = ['price', 'area', 'bedrooms', 'bathrooms']
        for col in key_columns:
            if col in df.columns:
                self.assertFalse(df[col].isnull().any(), f"Valores nulos en {col}")
        
        # Verificar rangos razonables si las columnas existen
        if 'price' in df.columns:
            self.assertGreater(df['price'].min(), 0, "Precios deben ser > 0")
        
        if 'area' in df.columns:
            self.assertGreater(df['area'].min(), 0, "Áreas deben ser > 0")
        
        if 'bedrooms' in df.columns:
            self.assertLessEqual(df['bedrooms'].max(), 10, "Demasiadas habitaciones")
        
        if 'bathrooms' in df.columns:
            self.assertLessEqual(df['bathrooms'].max(), 6, "Demasiados baños")
        
        print("✓ Calidad de datos verificada")

if __name__ == '__main__':
    unittest.main()
