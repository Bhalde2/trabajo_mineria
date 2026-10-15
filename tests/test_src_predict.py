import unittest
import os
import sys

import pandas as pd
import joblib

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from predict import load_trained_model, predict_price

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'model.pkl')

SAMPLE = {
    'area': 7500, 'bedrooms': 4, 'bathrooms': 2, 'stories': 3,
    'mainroad': 'yes', 'guestroom': 'no', 'basement': 'no',
    'hotwaterheating': 'no', 'airconditioning': 'yes',
    'parking': 2, 'prefarea': 'yes', 'furnishingstatus': 'furnished'
}


class TestSrcPredict(unittest.TestCase):
    """Ejercita src/predict.py contra el modelo entrenado"""

    @classmethod
    def setUpClass(cls):
        cls.model = joblib.load(MODEL_PATH)

    def test_load_trained_model_returns_estimator(self):
        model = load_trained_model()
        self.assertTrue(hasattr(model, 'predict'))
        self.assertTrue(hasattr(model, 'feature_names_in_'))

    def test_predict_price_from_dict(self):
        price = predict_price(self.model, SAMPLE)
        self.assertGreater(price, 1_000_000)
        self.assertLess(price, 20_000_000)

    def test_predict_price_from_dataframe(self):
        price = predict_price(self.model, pd.DataFrame([SAMPLE]))
        self.assertAlmostEqual(
            price, predict_price(self.model, SAMPLE), delta=1
        )

    def test_missing_categorical_column_does_not_crash(self):
        # El modelo fue entrenado con get_dummies: una fila sin una categórica
        # debe rellenarse a cero, no reventar.
        partial = {k: v for k, v in SAMPLE.items() if k != 'prefarea'}
        price = predict_price(self.model, partial)
        self.assertGreater(price, 0)


if __name__ == '__main__':
    unittest.main()