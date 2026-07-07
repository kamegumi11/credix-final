from pathlib import Path

# Raiz do projeto credix
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Camadas de dados
DADOS_DIR = PROJECT_ROOT / "dados"
BRONZE_DIR = PROJECT_ROOT / "bronze"
SILVER_DIR = PROJECT_ROOT / "silver"
GOLD_DIR = PROJECT_ROOT / "gold"
ASSETS_DIR = PROJECT_ROOT / "assets"

# Arquivos Bronze
APPLICATION_TRAIN_RAW = BRONZE_DIR / "application_train.csv"
APPLICATION_TEST_RAW = BRONZE_DIR / "application_test.csv"
BUREAU_RAW = BRONZE_DIR / "bureau.csv"

# Arquivos Silver
APPLICATION_CLEAN = SILVER_DIR / "application_clean.csv"
BUREAU_CLEAN = SILVER_DIR / "bureau_clean.csv"

# Features intermediárias
APPLICATION_FEATURES = SILVER_DIR / "application_features.csv"
BUREAU_FEATURES = SILVER_DIR / "bureau_features.csv"

# Gold / ABT
ABT_FILE = GOLD_DIR / "abt.csv"

# Artefatos do modelo
MODEL_FILE = ASSETS_DIR / "modelo.pkl"
PREPROCESSOR_FILE = ASSETS_DIR / "preprocessor.pkl"
FEATURE_NAMES_FILE = ASSETS_DIR / "feature_names.json"
METRICS_FILE = ASSETS_DIR / "metrics.json"

# Variáveis selecionadas para modelo individual
NUMERIC_FEATURES = [
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "AMT_GOODS_PRICE",
    "IDADE",
    "TEMPO_EMPRESA",
    "CREDITO_RENDA",
    "PARCELA_RENDA",
    "BEM_RENDA",
    "RENDA_LIVRE",
    "COMPROMETIMENTO_RENDA",
    "PRAZO_ESTIMADO",
    "BUREAU_QTD_CREDITOS",
    "BUREAU_QTD_ATIVOS",
    "BUREAU_TOTAL_CREDITO",
    "BUREAU_TOTAL_DIVIDA",
    "BUREAU_DEBT_RATIO",
]

CATEGORICAL_FEATURES = [
    "NAME_EDUCATION_TYPE",
    "NAME_FAMILY_STATUS",
]

TARGET = "TARGET"
ID_COL = "SK_ID_CURR"


def ensure_dirs():
    """Garante que as pastas principais existam."""
    for path in [BRONZE_DIR, SILVER_DIR, GOLD_DIR, ASSETS_DIR]:
        path.mkdir(parents=True, exist_ok=True)
