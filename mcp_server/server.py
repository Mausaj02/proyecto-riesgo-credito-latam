"""
Servidor MCP (Model Context Protocol) - Analista de Riesgo Crediticio LATAM
Expone la cartera de créditos procesada para que un asistente de IA
pueda hacer consultas analíticas en lenguaje natural.
"""

import json
import os
import pandas as pd
from mcp.server.fastmcp import FastMCP

# 1. Inicializar el servidor MCP
mcp = FastMCP("RiesgoCrediticioLATAM")

# 2. Definir la ruta del dataset limpio generado en la Fase 2 (ETL)
RUTA_DATOS = os.path.join("data", "processed", "creditos_latam_limpio.csv")


def cargar_cartera() -> pd.DataFrame:
    """Función auxiliar para cargar los datos procesados desde la carpeta local."""
    if not os.path.exists(RUTA_DATOS):
        raise FileNotFoundError(
            f"No se encontró el archivo de datos procesados en: {RUTA_DATOS}. "
            "Asegúrate de haber ejecutado el script etl_credit_risk.py en la Fase 2."
        )
    return pd.read_csv(RUTA_DATOS)


# ------------------------------------------------------------------
# HERRAMIENTAS (TOOLS) EXPUESTAS AL MODELO DE IA
# ------------------------------------------------------------------


@mcp.tool()
def obtener_kpis_generales() -> str:
    """
    Devuelve un resumen con los indicadores globales de la cartera de crédito:
    monto total desembolsado, cantidad de operaciones y porcentaje de morosidad (% Default).
    """
    df = cargar_cartera()
    total_creditos = len(df)
    casos_default = int(df["Indicador_Default"].sum())
    tasa_default = float((casos_default / total_creditos) * 100)
    monto_total = float(df["loan_amnt"].sum())

    resultado = {
        "total_creditos": total_creditos,
        "monto_total_desembolsado_usd": round(monto_total, 2),
        "creditos_en_default": casos_default,
        "tasa_morosidad_pct": round(tasa_default, 2),
    }
    return json.dumps(resultado, indent=2)


@mcp.tool()
def consultar_cliente_por_id(id_credito: str) -> str:
    """
    Busca y devuelve el expediente completo de riesgo de un crédito según su ID único (Ejemplo: 'CRD-1000').
    Permite auditar ingresos, tasa de interés, ratio DTI y estado de pago.
    """
    df = cargar_cartera()
    cliente = df[df["ID_Credito"] == id_credito]

    if cliente.empty:
        return json.dumps(
            {
                "error": f"No se encontró ningún crédito registrado con el ID '{id_credito}'."
            }
        )

    registro = cliente.iloc[0].to_dict()
    return json.dumps(registro, indent=2, default=str)


@mcp.tool()
def consultar_riesgo_por_nivel(nivel_riesgo: str) -> str:
    """
    Filtra la cartera según la categoría de riesgo ('Riesgo Bajo', 'Riesgo Medio', 'Riesgo Alto')
    y devuelve el volumen de créditos, monto expuesto y tasa de incumplimiento de ese segmento.
    """
    df = cargar_cartera()
    segmento = df[df["Nivel_Riesgo"].str.lower() == nivel_riesgo.lower()]

    if segmento.empty:
        return json.dumps(
            {
                "error": f"No se encontraron registros para la categoría de riesgo: '{nivel_riesgo}'."
            }
        )

    total_segmento = len(segmento)
    defaults_segmento = int(segmento["Indicador_Default"].sum())
    tasa_mora = (
        (defaults_segmento / total_segmento) * 100 if total_segmento > 0 else 0
    )

    resultado = {
        "nivel_riesgo": nivel_riesgo,
        "total_creditos": total_segmento,
        "creditos_en_default": defaults_segmento,
        "tasa_morosidad_pct": round(tasa_mora, 2),
        "monto_expuesto_usd": round(float(segmento["loan_amnt"].sum()), 2),
    }
    return json.dumps(resultado, indent=2)


if __name__ == "__main__":
    mcp.run()