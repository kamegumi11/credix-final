import pandas as pd
from config import (
    ensure_dirs,
    APPLICATION_TRAIN_RAW,
    BUREAU_RAW,
    APPLICATION_CLEAN,
    BUREAU_CLEAN,
)


def sanitize_application():
    print("Lendo application_train.csv da camada Bronze...")
    df = pd.read_csv(APPLICATION_TRAIN_RAW)

    print(f"Application original: {df.shape}")
    df = df.drop_duplicates()

    # Valor sentinela conhecido da base Home Credit: pensionistas/sem emprego informado
    if "DAYS_EMPLOYED" in df.columns:
        df["DAYS_EMPLOYED"] = df["DAYS_EMPLOYED"].replace(365243, pd.NA)

    # Padroniza textos vazios em colunas categóricas
    object_cols = df.select_dtypes(include="object").columns
    for col in object_cols:
        df[col] = df[col].fillna("Unknown")

    print(f"Application limpo: {df.shape}")
    df.to_csv(APPLICATION_CLEAN, index=False)
    print(f"Arquivo salvo em: {APPLICATION_CLEAN}")


def sanitize_bureau():
    print("Lendo bureau.csv da camada Bronze...")
    df = pd.read_csv(BUREAU_RAW)

    print(f"Bureau original: {df.shape}")
    df = df.drop_duplicates()

    object_cols = df.select_dtypes(include="object").columns
    for col in object_cols:
        df[col] = df[col].fillna("Unknown")

    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        df[col] = df[col].fillna(0)

    print(f"Bureau limpo: {df.shape}")
    df.to_csv(BUREAU_CLEAN, index=False)
    print(f"Arquivo salvo em: {BUREAU_CLEAN}")


def main():
    ensure_dirs()
    sanitize_application()
    sanitize_bureau()
    print("Sanitização concluída com sucesso.")


if __name__ == "__main__":
    main()
