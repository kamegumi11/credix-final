import pandas as pd
from config import BUREAU_CLEAN, BUREAU_FEATURES


def main():
    print("Gerando features da base bureau...")
    bureau = pd.read_csv(BUREAU_CLEAN)

    bureau["ATIVO"] = (bureau["CREDIT_ACTIVE"] == "Active").astype(int)

    qtd_creditos = bureau.groupby("SK_ID_CURR").size().rename("BUREAU_QTD_CREDITOS")
    qtd_ativos = bureau.groupby("SK_ID_CURR")["ATIVO"].sum().rename("BUREAU_QTD_ATIVOS")
    credito_total = bureau.groupby("SK_ID_CURR")["AMT_CREDIT_SUM"].sum().rename("BUREAU_TOTAL_CREDITO")
    divida_total = bureau.groupby("SK_ID_CURR")["AMT_CREDIT_SUM_DEBT"].sum().rename("BUREAU_TOTAL_DIVIDA")

    features = pd.concat([qtd_creditos, qtd_ativos, credito_total, divida_total], axis=1).reset_index()
    features["BUREAU_DEBT_RATIO"] = features["BUREAU_TOTAL_DIVIDA"] / features["BUREAU_TOTAL_CREDITO"].replace(0, 1)
    features["BUREAU_DEBT_RATIO"] = features["BUREAU_DEBT_RATIO"].fillna(0).clip(lower=0)

    features.to_csv(BUREAU_FEATURES, index=False)
    print(f"Bureau features salva em: {BUREAU_FEATURES}")
    print(features.shape)


if __name__ == "__main__":
    main()
