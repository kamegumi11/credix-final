import pandas as pd
from config import APPLICATION_CLEAN, APPLICATION_FEATURES, ID_COL


def main():
    print("Gerando features da base application...")
    df = pd.read_csv(APPLICATION_CLEAN)

    colunas = [
        "SK_ID_CURR",
        "TARGET",
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "AMT_GOODS_PRICE",
        "DAYS_BIRTH",
        "DAYS_EMPLOYED",
        "NAME_EDUCATION_TYPE",
        "NAME_FAMILY_STATUS",
    ]

    df = df[colunas].copy()

    # Garante que colunas numéricas estejam realmente como número
    numeric_cols = [
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "AMT_GOODS_PRICE",
        "DAYS_BIRTH",
        "DAYS_EMPLOYED",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Features de idade e tempo de empresa
    df["IDADE"] = df["DAYS_BIRTH"].abs() / 365
    df["TEMPO_EMPRESA"] = df["DAYS_EMPLOYED"].abs() / 365
    df["TEMPO_EMPRESA"] = df["TEMPO_EMPRESA"].fillna(0)

    # Features financeiras
    renda = df["AMT_INCOME_TOTAL"].replace(0, pd.NA)

    df["CREDITO_RENDA"] = df["AMT_CREDIT"] / renda
    df["PARCELA_RENDA"] = df["AMT_ANNUITY"] / renda
    df["BEM_RENDA"] = df["AMT_GOODS_PRICE"] / renda
    df["RENDA_LIVRE"] = df["AMT_INCOME_TOTAL"] - df["AMT_ANNUITY"]
    df["COMPROMETIMENTO_RENDA"] = (df["AMT_ANNUITY"] / renda).fillna(0)
    df["PRAZO_ESTIMADO"] = (
        df["AMT_CREDIT"] / df["AMT_ANNUITY"].replace(0, pd.NA)
    ).fillna(0)

    # Remove colunas originais de dias
    df.drop(columns=["DAYS_BIRTH", "DAYS_EMPLOYED"], inplace=True)

    # Trata nulos e valores inválidos
    ratio_cols = [
        "CREDITO_RENDA",
        "PARCELA_RENDA",
        "BEM_RENDA",
        "COMPROMETIMENTO_RENDA",
        "PRAZO_ESTIMADO",
    ]

    for col in ratio_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(0)
        df[col] = df[col].clip(lower=0)

    # Arredondamento
    float_cols = [
        "IDADE",
        "TEMPO_EMPRESA",
        "CREDITO_RENDA",
        "PARCELA_RENDA",
        "BEM_RENDA",
        "COMPROMETIMENTO_RENDA",
        "PRAZO_ESTIMADO",
    ]

    df[float_cols] = df[float_cols].round(2)

    # Garante categorias preenchidas
    df["NAME_EDUCATION_TYPE"] = df["NAME_EDUCATION_TYPE"].fillna("Unknown")
    df["NAME_FAMILY_STATUS"] = df["NAME_FAMILY_STATUS"].fillna("Unknown")

    assert df[ID_COL].is_unique, "SK_ID_CURR deveria ser único na application_features"

    df.to_csv(APPLICATION_FEATURES, index=False)
    print(f"Application features salva em: {APPLICATION_FEATURES}")
    print(df.shape)


if __name__ == "__main__":
    main()