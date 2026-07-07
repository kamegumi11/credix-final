# Credix MLOps

## 1. Objetivo da Arquitetura

A arquitetura da solução Credix foi desenhada para simular um ciclo real de Machine Learning em ambiente corporativo, contemplando ingestão de dados, tratamento, criação da ABT, treinamento do modelo, geração de artefatos, deploy via API, interface de negócio e monitoramento.

O objetivo é permitir que a empresa Credix estime a probabilidade de inadimplência de clientes, apoie decisões de concessão de crédito e automatize ações de acordo com a faixa de risco prevista pelo modelo.

---

## 2. Visão Geral da Arquitetura

```text
Kaggle / Home Credit Default Risk
        ↓
Camada Bronze
Dados brutos
        ↓
Camada Silver
Dados limpos e padronizados
        ↓
Camada Gold
ABT - Analytical Base Table
        ↓
Treinamento XGBoost
        ↓
Artefatos do modelo
modelo.pkl
preprocessor.pkl
feature_names.json
metrics.json
        ↓
FastAPI
Serviço de predição
        ↓
Streamlit
Interface para o usuário de negócio
        ↓
Monitoramento
Data Drift, PSI, métricas do modelo e alertas