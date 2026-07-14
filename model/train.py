import sys
import json
import pickle
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

# Raiz do projeto
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Coloca a raiz no path para importar datapipeline.config corretamente
sys.path.insert(0, str(PROJECT_ROOT))

from datapipeline.config import (
    ABT_FILE,
    MODEL_FILE,
    PREPROCESSOR_FILE,
    FEATURE_NAMES_FILE,
    METRICS_FILE,
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
    TARGET,
    ensure_dirs,
)


def main():
    ensure_dirs()

    print("Lendo ABT...")
    df = pd.read_csv(ABT_FILE)

    features = NUMERIC_FEATURES + CATEGORICAL_FEATURES

    print("Variáveis utilizadas no modelo:")
    for feature in features:
        print(f"- {feature}")

    X = df[features].copy()
    y = df[TARGET].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERIC_FEATURES),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )

    print("Aplicando pré-processamento...")
    X_train_t = preprocessor.fit_transform(X_train)
    X_test_t = preprocessor.transform(X_test)

    model = XGBClassifier(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="binary:logistic",
    eval_metric="auc",
    random_state=42,
    n_jobs=-1,
    scale_pos_weight=12
    )

    print("Treinando modelo XGBoost...")
    model.fit(X_train_t, y_train)

    proba = model.predict_proba(X_test_t)[:, 1]
    pred = (proba >= 0.5).astype(int)

    metrics = {
        "auc": float(roc_auc_score(y_test, proba)),
        "precision": float(precision_score(y_test, pred, zero_division=0)),
        "recall": float(recall_score(y_test, pred, zero_division=0)),
        "f1": float(f1_score(y_test, pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
        "threshold": 0.08,
        "features": features,
    }

    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)

    with open(PREPROCESSOR_FILE, "wb") as f:
        pickle.dump(preprocessor, f)

    with open(FEATURE_NAMES_FILE, "w", encoding="utf-8") as f:
        json.dump(features, f, ensure_ascii=False, indent=2)

    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    print("Modelo salvo em:", MODEL_FILE)
    print("Preprocessor salvo em:", PREPROCESSOR_FILE)
    print("Features salvas em:", FEATURE_NAMES_FILE)
    print("Métricas salvas em:", METRICS_FILE)

    print("Métricas:")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()