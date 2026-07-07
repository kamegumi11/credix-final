import sys
import json
import pickle
from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# Define raiz do projeto
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from datapipeline.config import (
    MODEL_FILE,
    PREPROCESSOR_FILE,
    FEATURE_NAMES_FILE,
)


app = FastAPI(
    title="Credix - API de Risco de Crédito",
    description="API para predição de probabilidade de inadimplência usando modelo XGBoost.",
    version="1.0.0",
)


class CreditRequest(BaseModel):
    AMT_INCOME_TOTAL: float
    AMT_CREDIT: float
    AMT_ANNUITY: float
    AMT_GOODS_PRICE: float
    IDADE: float
    TEMPO_EMPRESA: float
    CREDITO_RENDA: float
    PARCELA_RENDA: float
    BEM_RENDA: float
    RENDA_LIVRE: float
    COMPROMETIMENTO_RENDA: float
    PRAZO_ESTIMADO: float
    BUREAU_QTD_CREDITOS: float
    BUREAU_QTD_ATIVOS: float
    BUREAU_TOTAL_CREDITO: float
    BUREAU_TOTAL_DIVIDA: float
    BUREAU_DEBT_RATIO: float
    NAME_EDUCATION_TYPE: str
    NAME_FAMILY_STATUS: str


def load_artifacts():
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)

    with open(PREPROCESSOR_FILE, "rb") as f:
        preprocessor = pickle.load(f)

    with open(FEATURE_NAMES_FILE, "r", encoding="utf-8") as f:
        feature_names = json.load(f)

    return model, preprocessor, feature_names


model, preprocessor, feature_names = load_artifacts()


@app.get("/")
def home():
    return {
        "mensagem": "API Credix ativa",
        "modelo": "XGBoost",
        "status": "online",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "modelo_carregado": True,
        "quantidade_variaveis": len(feature_names),
    }


@app.post("/predict")
def predict_credit_risk(request: CreditRequest):
    input_data = request.model_dump()

    df = pd.DataFrame([input_data])
    df = df[feature_names]

    X_transformed = preprocessor.transform(df)

    probability = float(model.predict_proba(X_transformed)[:, 1][0])

    if probability < 0.20:
        risk_level = "baixo risco"
        recommended_action = "aprovação automática sugerida"
    elif probability < 0.60:
        risk_level = "risco médio"
        recommended_action = "enviar para análise manual"
    else:
        risk_level = "alto risco"
        recommended_action = "reprovação ou análise restritiva sugerida"

    return {
        "probabilidade_inadimplencia": round(probability, 4),
        "faixa_risco": risk_level,
        "acao_recomendada": recommended_action,
    }