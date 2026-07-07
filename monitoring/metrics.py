from sklearn.metrics import (
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


def calculate_model_metrics(y_true, y_proba, threshold=0.5):
    """
    Calcula métricas de performance do modelo.

    Parâmetros:
    y_true: valores reais observados
    y_proba: probabilidades previstas pelo modelo
    threshold: ponto de corte para classificar inadimplência

    Retorno:
    dicionário com AUC, precision, recall, f1 e matriz de confusão
    """

    y_pred = (y_proba >= threshold).astype(int)

    metrics = {
        "auc": float(roc_auc_score(y_true, y_proba)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        "threshold": threshold,
    }

    return metrics


def compare_with_baseline(current_metrics, baseline_metrics):
    """
    Compara métricas atuais de produção com métricas baseline do treinamento.
    """

    comparison = {}

    for metric in ["auc", "precision", "recall", "f1"]:
        current_value = current_metrics.get(metric)
        baseline_value = baseline_metrics.get(metric)

        if current_value is not None and baseline_value is not None:
            comparison[metric] = {
                "baseline": baseline_value,
                "current": current_value,
                "difference": current_value - baseline_value,
            }

    return comparison