import pandas as pd
import numpy as np
import argparse
import os
from typing import Dict


def _generate_row(rng: np.random.Generator) -> Dict:
    # Numéricos
    area = int(max(500, rng.lognormal(mean=np.log(6000), sigma=0.5)))
    bedrooms = int(rng.choice([1, 2, 3, 4, 5, 6], p=[0.02, 0.15, 0.5, 0.25, 0.06, 0.02]))
    bathrooms = int(max(1, min(4, rng.poisson(1) + 1)))
    stories = int(rng.choice([1, 2, 3, 4], p=[0.3, 0.4, 0.2, 0.1]))
    parking = int(rng.choice([0, 1, 2, 3], p=[0.15, 0.5, 0.25, 0.1]))

    # Categóricas (yes/no)
    mainroad = rng.choice(['yes', 'no'], p=[0.9, 0.1])
    guestroom = rng.choice(['yes', 'no'], p=[0.12, 0.88])
    basement = rng.choice(['yes', 'no'], p=[0.25, 0.75])
    hotwaterheating = rng.choice(['yes', 'no'], p=[0.05, 0.95])
    airconditioning = rng.choice(['yes', 'no'], p=[0.35, 0.65])
    prefarea = rng.choice(['yes', 'no'], p=[0.3, 0.7])

    furnishingstatus = rng.choice(
        ['furnished', 'semi-furnished', 'unfurnished'], p=[0.25, 0.5, 0.25]
    )

    # Precio sintético correlacionado con características
    base_rate = float(rng.normal(loc=900.0, scale=150.0))
    price = area * base_rate
    price += bedrooms * 120_000
    price += bathrooms * 70_000
    price += parking * 60_000
    price += 200_000 if mainroad == 'yes' else 0
    price += 150_000 if prefarea == 'yes' else 0
    price += 150_000 if basement == 'yes' else 0
    price += 100_000 if airconditioning == 'yes' else 0

    if furnishingstatus == 'furnished':
        price += 150_000
    elif furnishingstatus == 'semi-furnished':
        price += 70_000

    # Ruido
    price += float(rng.normal(loc=0.0, scale=250_000.0))
    price = int(max(100_000, price))

    return {
        'price': price,
        'area': area,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'stories': stories,
        'mainroad': mainroad,
        'guestroom': guestroom,
        'basement': basement,
        'hotwaterheating': hotwaterheating,
        'airconditioning': airconditioning,
        'parking': parking,
        'prefarea': prefarea,
        'furnishingstatus': furnishingstatus,
    }


def generate_dataset(n_rows: int = 1000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = [_generate_row(rng) for _ in range(int(n_rows))]
    df = pd.DataFrame(rows)
    # Asegurar orden de columnas igual al CSV original
    cols = [
        'price', 'area', 'bedrooms', 'bathrooms', 'stories', 'mainroad',
        'guestroom', 'basement', 'hotwaterheating', 'airconditioning',
        'parking', 'prefarea', 'furnishingstatus'
    ]
    df = df[cols]
    return df


def save_dataset(df: pd.DataFrame, path: str) -> None:
    dirpath = os.path.dirname(path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    df.to_csv(path, index=False)


def _parse_args():
    parser = argparse.ArgumentParser(
        description='Generar un dataset sintético compatible con data/Housing.csv'
    )
    parser.add_argument('--n', type=int, default=1000, help='Número de filas a generar')
    parser.add_argument('--out', type=str, default='data/Housing.csv', help='Ruta de salida CSV')
    parser.add_argument('--seed', type=int, default=42, help='Seed aleatorio reproducible')
    return parser.parse_args()


if __name__ == '__main__':
    args = _parse_args()
    df = generate_dataset(n_rows=args.n, seed=args.seed)
    save_dataset(df, args.out)
    print(f"✅ Dataset generado: {args.out} ({len(df)} filas)")
