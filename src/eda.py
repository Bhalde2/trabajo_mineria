import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def main():
    print("Iniciando Análisis Exploratorio de Datos...")
    
    # Crear directorio de evidencias
    os.makedirs('../docs/pruebas', exist_ok=True)
    
    # Cargar datos
    df = pd.read_csv('data/Housing.csv')
    print("=== INFORMACIÓN DEL DATASET ===")
    print(f"Dimensiones: {df.shape}")
    print(f"Columnas: {df.columns.tolist()}")
    
    # Análisis básico
    print(f"\nPrecio promedio: Rs {df['price'].mean():,.2f}")
    print(f"Área promedio: {df['area'].mean():.0f} sq. ft")
    print(f"Correlación precio-área: {df['price'].corr(df['area']):.3f}")
    
    # Gráfico simple
    plt.figure(figsize=(10, 6))
    plt.scatter(df['area'], df['price'], alpha=0.6)
    plt.xlabel('Área (sq. ft)')
    plt.ylabel('Precio (Rs)')
    plt.title('Relación Precio vs Área')
    plt.savefig('docs/pruebas/precio_vs_area.png')
    plt.close()
    
    print("EDA completado. Gráfico guardado en docs/pruebas/")

if __name__ == "__main__":
    main()