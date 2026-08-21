# Credix MLOps

## 1. Objetivo da Arquitetura

A arquitetura da solução Credix foi desenhada para simular o ciclo de vida completo de uma aplicação de Machine Learning em ambiente corporativo, contemplando ingestão de dados, preparação, treinamento, deploy do modelo, monitoramento e evolução contínua.

O objetivo é permitir que empresas utilizem o modelo Credix para estimar a probabilidade de inadimplência de clientes e disponibilizar essa inteligência por meio de serviços de predição acessíveis por API.

---

## 2. Arquitetura da Solução

A solução foi estruturada em camadas que representam o fluxo completo desde a origem dos dados até a disponibilização do modelo como serviço de predição.

```text
Kaggle / Home Credit Default Risk
                │
                ▼
         Camada Bronze
          Dados Brutos
                │
                ▼
         Camada Silver
 Dados Tratados e Padronizados
                │
                ▼
          Camada Gold
   ABT (Analytical Base Table)
                │
                ▼
      Treinamento XGBoost
                │
                ▼
      Artefatos do Modelo
─────────────────────────────
modelo.pkl
preprocessor.pkl
feature_names.json
metrics.json
─────────────────────────────
                │
                ▼
             FastAPI
     Serviço de Predição
                │
                ▼
            Streamlit
 Interface para Usuário Final
                │
                ▼
             Consumo
      das Predições Geradas
```

### Componentes da Solução

**Camada Bronze**
- Armazena os dados brutos oriundos da base Home Credit Default Risk.

**Camada Silver**
- Realiza limpeza, tratamento e padronização dos dados.

**Camada Gold**
- Disponibiliza a ABT (Analytical Base Table) utilizada pelo modelo.

**Treinamento**
- Treina o modelo XGBoost utilizando os dados preparados.

**Artefatos**
- Armazena os arquivos necessários para inferência e monitoramento.

**FastAPI**
- Disponibiliza o modelo como serviço REST para consumo externo.

**Streamlit**
- Fornece uma interface de negócio para utilização das previsões.

**Docker Compose**
- Permite executar todos os componentes da solução de forma integrada.

**Apache Airflow**
- Responsável pela orquestração do pipeline de preparação de dados e treinamento.

---

## 3. Próximos Passos de Desenvolvimento

Como evolução para um ambiente produtivo, estão previstos mecanismos de monitoramento contínuo e automação baseada nas previsões do modelo.

### 3.1 Monitoramento dos Dados e do Modelo

O monitoramento tem como objetivo identificar problemas operacionais, degradação da performance do modelo e mudanças de comportamento dos dados utilizados nas previsões.

#### Monitoramento dos Dados

Serão monitorados indicadores estatísticos das principais variáveis de entrada:

- Média
- Mediana
- Desvio padrão
- Percentual de valores nulos
- Population Stability Index (PSI)

Esse acompanhamento permitirá identificar:

- Data Drift
- Mudanças no perfil dos clientes
- Alterações relevantes na distribuição das variáveis

#### Monitoramento do Modelo

Após a disponibilização do resultado real dos contratos, as previsões poderão ser comparadas com os resultados observados.

As métricas monitoradas incluem:

- Recall
- Precision
- F1-Score
- ROC AUC
- Taxa de falsos negativos

Esse acompanhamento permitirá identificar:

- Perda de performance do modelo
- Redução da capacidade de identificar inadimplentes
- Necessidade de retreinamento

#### Monitoramento Operacional

Também serão monitorados os componentes técnicos da solução:

- Falhas de execução do pipeline
- Falhas em DAGs do Airflow
- Indisponibilidade da API
- Tempo de resposta da aplicação
- Erros de execução dos containers

---

### 3.2 Ações Automatizadas e Agentes de IA

As previsões geradas pelo modelo poderão ser utilizadas para automatizar processos de negócio relacionados à concessão de crédito.

#### Clientes de Baixo Risco

- Aprovação automática da solicitação de crédito.

#### Clientes de Médio Risco

- Encaminhamento para análise complementar.
- Simulação automática de novas condições de crédito.
- Sugestão de valor ou prazo mais adequado ao perfil do cliente.

#### Clientes de Alto Risco

- Recusa automática da solicitação.
- Encaminhamento para análise especializada quando necessário.

#### Agente Explicador

Um agente de IA poderá utilizar informações de interpretabilidade do modelo (SHAP) para explicar, em linguagem natural, os fatores que mais influenciaram a decisão de crédito.

Exemplo:

"Seu pedido apresentou maior risco devido ao comprometimento de renda e ao histórico de endividamento atual."

#### Agente de Monitoramento

Um agente de IA poderá analisar automaticamente alertas relacionados a:

- Data Drift
- PSI elevado
- Queda de Recall
- Queda de ROC AUC
- Degradação geral da performance

Com base nessas análises, o agente poderá recomendar investigações adicionais e avaliar a necessidade de iniciar um novo ciclo de retreinamento do modelo.

---

## 4. Considerações Finais

A arquitetura proposta permite a construção de uma solução completa de Machine Learning, contemplando preparação dos dados, treinamento, disponibilização do modelo, monitoramento e evolução contínua.

A utilização de Airflow, Docker Compose, FastAPI e Streamlit fornece uma base adequada para simular um ambiente corporativo de operação de modelos analíticos, enquanto os mecanismos de monitoramento e automação representam a evolução necessária para um cenário produtivo de MLOps.