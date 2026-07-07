import pandas as pd
import numpy as np


def calculate_psi(expected, actual, buckets=10):
    """Calcula Population Stability Index para monitorar data drift."""
    expected = pd.Series(expected).dropna()
    actual = pd.Series(actual).dropna()

    breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))
    breakpoints = np.unique(breakpoints)

    if len(breakpoints) <= 2:
        return 0.0

    expected_counts = pd.cut(expected, bins=breakpoints, include_lowest=True).value_counts(sort=False)
    actual_counts = pd.cut(actual, bins=breakpoints, include_lowest=True).value_counts(sort=False)

    expected_pct = expected_counts / max(expected_counts.sum(), 1)
    actual_pct = actual_counts / max(actual_counts.sum(), 1)

    expected_pct = expected_pct.replace(0, 0.0001)
    actual_pct = actual_pct.replace(0, 0.0001)

    psi = ((actual_pct - expected_pct) * np.log(actual_pct / expected_pct)).sum()
    return float(psi)


def classify_psi(psi):
    if psi < 0.10:
        return "Sem drift relevante"
    if psi < 0.25:
        return "Atenção: possível drift"
    return "Drift forte: investigar/re-treinar"
