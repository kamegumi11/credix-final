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
