import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from src.services.cliente_service import listar_clientes_cache
from src.utils.validators import calcular_status_vencimento
from src.core.config import VERMELHO, AMARELO_ALERTA, VERDE_HULK, CINZA_MEDIO

def mostrar_dashboard():
    st.title("📊 Dashboard Financeiro")
    dados = listar_clientes_cache()
    if not dados:
        st.info("Nenhum aluno cadastrado.")
        return

    df = pd.DataFrame(dados)
    total_alunos = len(df)
    faturamento = df['mensalidade'].sum() if not df.empty else 0
    media_mensal = df['mensalidade'].mean() if not df.empty else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Alunos", total_alunos)
    col2.metric("Faturamento Mensal", f"R$ {faturamento:,.2f}")
    col3.metric("Mensalidade Média", f"R$ {media_mensal:,.2f}")

    st.subheader("🚨 Alertas de Vencimento")
    hoje = date.today()
    status_map = []
    prox_datas = []
    dias_rest = []

    for _, row in df.iterrows():
        info = calcular_status_vencimento(row['vencimento'])
        status_map.append(info["status"])
        prox_datas.append(info["prox_venc"])
        dias_rest.append(info["dias_rest"])

    df['status'] = status_map
    df['prox_venc'] = prox_datas
    df['dias_rest'] = dias_rest

    vencidos = len(df[df['status'] == 'vencido'])
    proximos = len(df[df['status'] == 'proximo'])
    em_dia = len(df[df['status'] == 'em_dia'])
    invalidos = len(df[df['status'] == 'data_invalida'])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔴 Vencidos", vencidos)
    c2.metric("🟡 Próximos (5 dias)", proximos)
    c3.metric("🟢 Em dia", em_dia)
    c4.metric("❌ Data inválida", invalidos)

    st.dataframe(df[['nome', 'mensalidade', 'vencimento', 'prox_venc', 'dias_rest', 'status']], use_container_width=True)

    if st.checkbox("Mostrar gráfico de status"):
        status_df = pd.DataFrame({
            'Status': ['Vencido', 'Próximo (5 dias)', 'Em dia', 'Data inválida'],
            'Quantidade': [vencidos, proximos, em_dia, invalidos]
        })
        fig = px.bar(status_df, x='Status', y='Quantidade', color='Status',
                     color_discrete_map={
                         'Vencido': VERMELHO,
                         'Próximo (5 dias)': AMARELO_ALERTA,
                         'Em dia': VERDE_HULK,
                         'Data inválida': CINZA_MEDIO
                     })
        st.plotly_chart(fig, use_container_width=True)
