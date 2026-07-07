import sys
import pickle
import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from datapipeline.config import (
    MODEL_FILE,
    PREPROCESSOR_FILE,
    FEATURE_NAMES_FILE,
)


def load_artifacts():
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)

    with open(PREPROCESSOR_FILE, "rb") as f:
        preprocessor = pickle.load(f)

    with open(FEATURE_NAMES_FILE, "r", encoding="utf-8") as f:
        features = json.load(f)

    return model, preprocessor, features


def predict_one(input_data: dict):
    model, preprocessor, features = load_artifacts()

    df = pd.DataFrame([input_data])
    df = df[features]

    X_t = preprocessor.transform(df)
    proba = float(model.predict_proba(X_t)[:, 1][0])

    if proba < 0.20:
        faixa = "baixo risco"
        acao = "aprovação automática sugerida"
    elif proba < 0.60:
        faixa = "risco médio"
        acao = "enviar para análise manual"
    else:
        faixa = "alto risco"
        acao = "reprovação ou análise restritiva sugerida"

    return {
        "probabilidade_inadimplencia": round(proba, 4),
        "faixa_risco": faixa,
        "acao_recomendada": acao,
    }


if __name__ == "__main__":
    exemplo = {
        "AMT_INCOME_TOTAL": 150000,
        "AMT_CREDIT": 500000,
        "AMT_ANNUITY": 25000,
        "AMT_GOODS_PRICE": 450000,
        "IDADE": 35,
        "TEMPO_EMPRESA": 5,
        "CREDITO_RENDA": 3.33,
        "PARCELA_RENDA": 0.17,
        "BEM_RENDA": 3.0,
        "RENDA_LIVRE": 125000,
        "COMPROMETIMENTO_RENDA": 0.17,
        "PRAZO_ESTIMADO": 20,
        "BUREAU_QTD_CREDITOS": 3,
        "BUREAU_QTD_ATIVOS": 1,
        "BUREAU_TOTAL_CREDITO": 200000,
        "BUREAU_TOTAL_DIVIDA": 50000,
        "BUREAU_DEBT_RATIO": 0.25,
        "NAME_EDUCATION_TYPE": "Higher education",
        "NAME_FAMILY_STATUS": "Married",
    }

    resultado = predict_one(exemplo)
    print(resultado)