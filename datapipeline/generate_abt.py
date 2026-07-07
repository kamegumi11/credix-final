import pandas as pd
from config import APPLICATION_FEATURES, BUREAU_FEATURES, ABT_FILE, ID_COL


def main():
    print("Gerando ABT na camada Gold...")
    app = pd.read_csv(APPLICATION_FEATURES)
    bureau = pd.read_csv(BUREAU_FEATURES)

    abt = app.merge(bureau, on=ID_COL, how="left")

    bureau_cols = [c for c in abt.columns if c.startswith("BUREAU_")]
    abt[bureau_cols] = abt[bureau_cols].fillna(0)

    assert abt[ID_COL].is_unique, "SK_ID_CURR deveria ser único na ABT"

    abt.to_csv(ABT_FILE, index=False)
    print(f"ABT salva em: {ABT_FILE}")
    print(abt.shape)


if __name__ == "__main__":
    main()
