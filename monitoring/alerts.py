def evaluate_psi_alert(psi_value):
    """
    Avalia nível de alerta com base no PSI.
    """

    if psi_value < 0.10:
        return {
            "nivel": "normal",
            "mensagem": "Sem drift relevante detectado.",
            "acao": "Manter monitoramento contínuo.",
        }

    elif psi_value < 0.25:
        return {
            "nivel": "atenção",
            "mensagem": "Possível mudança no perfil dos dados.",
            "acao": "Investigar variáveis com maior alteração.",
        }

    else:
        return {
            "nivel": "crítico",
            "mensagem": "Drift forte detectado.",
            "acao": "Avaliar retreinamento do modelo.",
        }


def evaluate_performance_alert(current_auc, baseline_auc, tolerance=0.05):
    """
    Avalia perda de performance do modelo com base na queda de AUC.
    """

    auc_drop = baseline_auc - current_auc

    if auc_drop <= tolerance:
        return {
            "nivel": "normal",
            "mensagem": "Performance dentro do esperado.",
            "acao": "Manter modelo em produção.",
            "auc_drop": auc_drop,
        }

    else:
        return {
            "nivel": "crítico",
            "mensagem": "Queda relevante de performance detectada.",
            "acao": "Investigar dados recentes e considerar retreinamento.",
            "auc_drop": auc_drop,
        }


def evaluate_api_latency(latency_ms, threshold_ms=500):
    """
    Avalia latência da API.
    """

    if latency_ms <= threshold_ms:
        return {
            "nivel": "normal",
            "mensagem": "Latência dentro do limite esperado.",
            "acao": "Nenhuma ação necessária.",
            "latency_ms": latency_ms,
        }

    else:
        return {
            "nivel": "atenção",
            "mensagem": "Latência acima do limite esperado.",
            "acao": "Verificar infraestrutura, logs e volume de chamadas.",
            "latency_ms": latency_ms,
        }