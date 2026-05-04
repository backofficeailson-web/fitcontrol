import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from src.services.cliente_service import listar_clientes_cache
from src.utils.validators import calcular_status_vencimento

def mostrar_dashboard():
    st.title("📊 Dashboard")
    
    dados = listar_clientes_cache()
    if not dados:
        st.info("Nenhum aluno cadastrado. Acesse 'Alunos' para cadastrar.")
        return

    df = pd.DataFrame(dados)
    total_alunos = len(df)
    faturamento = df['mensalidade'].sum() if not df.empty else 0
    media_mensal = df['mensalidade'].mean() if not df.empty else 0

    # Cards principais
    c1, c2, c3 = st.columns(3)
    c1.metric("👥 Alunos ativos", total_alunos)
    c2.metric("💰 Faturamento", f"R$ {faturamento:,.2f}")
    c3.metric("📊 Ticket médio", f"R$ {media_mensal:,.2f}")

    st.markdown("---")
    st.subheader("🚨 Vencimentos")
    
    hoje = date.today()
    status_list = []
    for _, row in df.iterrows():
        info = calcular_status_vencimento(row['vencimento'])
        status_list.append(info)
    
    df['status'] = [s['status'] for s in status_list]
    df['prox_venc'] = [s['prox_venc'] for s in status_list]

    vencidos = len(df[df['status'] == 'vencido'])
    proximos = len(df[df['status'] == 'proximo'])
    em_dia = len(df[df['status'] == 'em_dia'])

    col1, col2, col3 = st.columns(3)
    col1.metric("🔴 Vencidos", vencidos)
    col2.metric("🟡 A vencer (5d)", proximos)
    col3.metric("🟢 Em dia", em_dia)

    # Tabela resumida
    st.dataframe(
        df[['nome', 'mensalidade', 'vencimento', 'prox_venc', 'status']].head(10),
        use_container_width=True
    )

    # Gráfico opcional
    if st.checkbox("Mostrar gráfico"):
        fig = px.bar(
            x=['Vencidos', 'A vencer', 'Em dia'],
            y=[vencidos, proximos, em_dia],
            color=['Vencidos', 'A vencer', 'Em dia'],
            color_discrete_map={'Vencidos': '#F87171', 'A vencer': '#FBBF24', 'Em dia': '#4ADE80'}
        )
        fig.update_layout(
            plot_bgcolor='#111111',
            paper_bgcolor='#111111',
            font_color='#E5E7EB',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
