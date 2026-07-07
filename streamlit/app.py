import os
import requests
import streamlit as st


st.set_page_config(
    page_title="Credix - Risco de Crédito",
    page_icon="💳",
    layout="centered",
)

st.title("💳 Credix - Predição de Risco de Crédito")

st.markdown(
    """
    Esta aplicação simula o uso do modelo de Machine Learning da Credix para estimar
    a probabilidade de inadimplência de um cliente.

    O Streamlit envia os dados para a API FastAPI, que carrega o modelo treinado
    salvo em `assets/modelo.pkl`.
    """
)

st.divider()

st.sidebar.header("Configuração da API")

default_api_url = os.getenv("API_URL", "http://127.0.0.1:8000/predict")

api_url = st.sidebar.text_input(
    "URL da API",
    value=default_api_url,
)

st.header("Dados do cliente")

col1, col2 = st.columns(2)

with col1:
    renda_anual = st.number_input(
        "Renda anual",
        min_value=0.0,
        value=150000.0,
        step=1000.0,
    )

    valor_credito = st.number_input(
        "Valor do crédito solicitado",
        min_value=0.0,
        value=500000.0,
        step=1000.0,
    )

    valor_parcela = st.number_input(
        "Valor da parcela anualizada",
        min_value=0.0,
        value=25000.0,
        step=500.0,
    )

    valor_bem = st.number_input(
        "Valor do bem",
        min_value=0.0,
        value=450000.0,
        step=1000.0,
    )

with col2:
    idade = st.number_input(
        "Idade",
        min_value=18.0,
        max_value=100.0,
        value=35.0,
        step=1.0,
    )

    tempo_empresa = st.number_input(
        "Tempo de empresa / ocupação em anos",
        min_value=0.0,
        max_value=60.0,
        value=5.0,
        step=1.0,
    )

    escolaridade = st.selectbox(
        "Escolaridade",
        [
            "Secondary / secondary special",
            "Higher education",
            "Incomplete higher",
            "Lower secondary",
            "Academic degree",
            "Unknown",
        ],
        index=1,
    )

    estado_civil = st.selectbox(
        "Estado civil",
        [
            "Married",
            "Single / not married",
            "Civil marriage",
            "Separated",
            "Widow",
            "Unknown",
        ],
        index=0,
    )

st.header("Histórico de crédito - Bureau")

col3, col4 = st.columns(2)

with col3:
    bureau_qtd_creditos = st.number_input(
        "Quantidade de créditos no bureau",
        min_value=0.0,
        value=3.0,
        step=1.0,
    )

    bureau_qtd_ativos = st.number_input(
        "Quantidade de créditos ativos",
        min_value=0.0,
        value=1.0,
        step=1.0,
    )

with col4:
    bureau_total_credito = st.number_input(
        "Total de crédito no bureau",
        min_value=0.0,
        value=200000.0,
        step=1000.0,
    )

    bureau_total_divida = st.number_input(
        "Total de dívida no bureau",
        min_value=0.0,
        value=50000.0,
        step=1000.0,
    )

st.divider()

if st.button("🔍 Calcular risco de inadimplência", type="primary"):
    if renda_anual == 0:
        st.error("A renda anual precisa ser maior que zero.")
    elif valor_parcela == 0:
        st.error("O valor da parcela precisa ser maior que zero.")
    else:
        credito_renda = valor_credito / renda_anual
        parcela_renda = valor_parcela / renda_anual
        bem_renda = valor_bem / renda_anual
        renda_livre = renda_anual - valor_parcela
        comprometimento_renda = valor_parcela / renda_anual
        prazo_estimado = valor_credito / valor_parcela

        if bureau_total_credito == 0:
            bureau_debt_ratio = 0
        else:
            bureau_debt_ratio = bureau_total_divida / bureau_total_credito

        payload = {
            "AMT_INCOME_TOTAL": renda_anual,
            "AMT_CREDIT": valor_credito,
            "AMT_ANNUITY": valor_parcela,
            "AMT_GOODS_PRICE": valor_bem,
            "IDADE": idade,
            "TEMPO_EMPRESA": tempo_empresa,
            "CREDITO_RENDA": credito_renda,
            "PARCELA_RENDA": parcela_renda,
            "BEM_RENDA": bem_renda,
            "RENDA_LIVRE": renda_livre,
            "COMPROMETIMENTO_RENDA": comprometimento_renda,
            "PRAZO_ESTIMADO": prazo_estimado,
            "BUREAU_QTD_CREDITOS": bureau_qtd_creditos,
            "BUREAU_QTD_ATIVOS": bureau_qtd_ativos,
            "BUREAU_TOTAL_CREDITO": bureau_total_credito,
            "BUREAU_TOTAL_DIVIDA": bureau_total_divida,
            "BUREAU_DEBT_RATIO": bureau_debt_ratio,
            "NAME_EDUCATION_TYPE": escolaridade,
            "NAME_FAMILY_STATUS": estado_civil,
        }

        try:
            response = requests.post(api_url, json=payload, timeout=10)

            if response.status_code == 200:
                result = response.json()

                probabilidade = result["probabilidade_inadimplencia"]
                faixa_risco = result["faixa_risco"]
                acao = result["acao_recomendada"]

                st.success("Predição realizada com sucesso!")

                st.metric(
                    label="Probabilidade de inadimplência",
                    value=f"{probabilidade:.2%}",
                )

                if faixa_risco == "baixo risco":
                    st.info(f"Faixa de risco: {faixa_risco}")
                elif faixa_risco == "risco médio":
                    st.warning(f"Faixa de risco: {faixa_risco}")
                else:
                    st.error(f"Faixa de risco: {faixa_risco}")

                st.subheader("Ação recomendada")
                st.write(acao)

                with st.expander("Ver payload enviado para a API"):
                    st.json(payload)

                with st.expander("Ver resposta completa da API"):
                    st.json(result)

            else:
                st.error(f"Erro na API. Status code: {response.status_code}")
                st.text(response.text)

        except requests.exceptions.ConnectionError:
            st.error(
                "Não foi possível conectar à API. "
                "Verifique se a FastAPI está rodando em http://127.0.0.1:8000."
            )

        except Exception as e:
            st.error("Erro inesperado ao chamar a API.")
            st.exception(e)

st.divider()

st.caption(
    "Credix | Projeto LabFIA | Pipeline Bronze, Silver, Gold, XGBoost, FastAPI e Streamlit"
)