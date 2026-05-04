# src/pages/dashboard_page.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from src.services.cliente_service import listar_clientes_cache
from src.utils.validators import calcular_status_vencimento
from src.core.config import VERMELHO, AMARELO_ALERTA, VERDE_HULK, CINZA_MEDIO

def mostrar_dashboard():
    st.title("📊 Dashboard")
    st.markdown("---")
    
    dados = listar_clientes_cache()
    if not dados:
        st.info("Nenhum aluno cadastrado.")
        return

    df = pd.DataFrame(dados)
    total_alunos = len(df)
    faturamento = df['mensalidade'].sum() if not df.empty else 0
    media_mensal = df['mensalidade'].mean() if not df.empty else 0

    # Cards principais
    c1, c2, c3 = st.columns(3)
    c1.metric("👥 Total de Alunos", total_alunos)
    c2.metric("💰 Faturamento Mensal", f"R$ {faturamento:,.2f}")
    c3.metric("📊 Mensalidade Média", f"R$ {media_mensal:,.2f}")

    # Alertas de vencimento
    st.subheader("🚨 Alertas de Vencimento")
    hoje = date.today()
    status_map = []
    for _, row in df.iterrows():
        info = calcular_status_vencimento(row['vencimento'])
        status_map.append(info)
    
    df['status'] = [s['status'] for s in status_map]
    df['prox_venc'] = [s['prox_venc'] for s in status_map]

    vencidos = len(df[df['status'] == 'vencido'])
    proximos = len(df[df['status'] == 'proximo'])
    em_dia = len(df[df['status'] == 'em_dia'])
    invalidos = len(df[df['status'] == 'data_invalida'])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🔴 Vencidos", vencidos)
    col2.metric("🟡 Próximos (5d)", proximos)
    col3.metric("🟢 Em dia", em_dia)
    col4.metric("❌ Inválidos", invalidos)

    # Tabela resumida
    st.dataframe(
        df[['nome', 'mensalidade', 'vencimento', 'prox_venc', 'status']],
        use_container_width=True
    )

    # Gráfico de status (opcional)
    if st.checkbox("Mostrar gráfico de status"):
        status_df = pd.DataFrame({
            'Status': ['Vencido', 'Próximo (5d)', 'Em dia', 'Data inválida'],
            'Quantidade': [vencidos, proximos, em_dia, invalidos]
        })
        fig = px.bar(status_df, x='Status', y='Quantidade', color='Status',
                     color_discrete_map={
                         'Vencido': VERMELHO,
                         'Próximo (5d)': AMARELO_ALERTA,
                         'Em dia': VERDE_HULK,
                         'Data inválida': CINZA_MEDIO
                     })
        st.plotly_chart(fig, use_container_width=True)
