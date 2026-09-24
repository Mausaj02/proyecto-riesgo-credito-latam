import os
import kagglehub
import numpy as np
import pandas as pd

# 1. Descarga automática del dataset desde Kaggle
print(" Descargando dataset desde Kaggle...")
path = kagglehub.dataset_download("laotse/credit-risk-dataset")
print(" Archivo descargado en:", path)

# 2. Cargar el archivo CSV descargado
archivo_csv = os.path.join(path, "credit_risk_dataset.csv")
df = pd.read_csv(archivo_csv)

# 3. Limpieza y Creación de Indicadores de Riesgo
# Imputación de nulos
df["person_emp_length"].fillna(df["person_emp_length"].median(), inplace=True)
df["loan_int_rate"].fillna(df["loan_int_rate"].median(), inplace=True)

# Cálculo de DTI (Debt-to-Income)
df["Ratio_DTI"] = np.where(
    df["person_income"] > 0,
    (df["loan_amnt"] / df["person_income"]).round(4),
    0,
)

# Flag de Default
df["Indicador_Default"] = df["loan_status"].astype(int)

# Clasificación de Riesgo
condiciones = [
    (df["loan_int_rate"] < 10.0),
    (df["loan_int_rate"] >= 10.0) & (df["loan_int_rate"] < 15.0),
    (df["loan_int_rate"] >= 15.0),
]
niveles = ["Riesgo Bajo", "Riesgo Medio", "Riesgo Alto"]
df["Nivel_Riesgo"] = np.select(condiciones, niveles, default="Sin Clasificar")

# ID Único de Crédito
df.insert(0, "ID_Credito", [f"CRD-{1000 + i}" for i in range(len(df))])

# 4. Guardar dataset limpio en la carpeta del proyecto
ruta_salida = "data/processed/creditos_latam_limpio.csv"
os.makedirs("data/processed", exist_ok=True)
df.to_csv(ruta_salida, index=False)

# 5. Resumen en consola
print("\n" + "=" * 40)
print("   PROCESAMIENTO ETL COMPLETADO")
print("=" * 40)
print(f" Total de Créditos : {len(df):,}")
print(f" % Morosidad       : {(df['Indicador_Default'].mean() * 100):.2f}%")
print(f" Archivo guardado  : {ruta_salida}")
print("=" * 40)