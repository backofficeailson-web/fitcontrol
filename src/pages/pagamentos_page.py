import streamlit as st
import pandas as pd
from datetime import date
from src.core.database import execute_query
from src.core.state import bump_cache
from src.services.cliente_service import listar_clientes_select_cache
from src.ui.feedback import sucesso, erro, aviso
from src.ui.pagination import paginated_dataframe, renderizar_controles_paginacao
import logging

logger = logging.getLogger(__name__)

_Q_INSERIR = "INSERT INTO pagamentos (cliente_id, data, valor, status, forma, observacao) VALUES (?,?,?,?,?,?)"
_Q_HISTORICO = """
    SELECT p.id, c.nome AS cliente, p.data, p.valor, p.status, p.forma, p.observacao
    FROM pagamentos p JOIN clientes c ON c.id = p.cliente_id WHERE 1=1
"""
_Q_COUNT = "SELECT COUNT(*) as total FROM pagamentos p JOIN clientes c ON c.id = p.cliente_id WHERE 1=1"

def pagina_pagamentos():
    st.title("💰 Pagamentos")
    tab1, tab2 = st.tabs(["📝 Registrar", "📋 Histórico"])

    with tab1:
        clientes = listar_clientes_select_cache()
        if not clientes:
            aviso("Nenhum aluno ativo.")
            return
        opcoes = {c["nome"]: c["id"] for c in clientes}
        with st.form("form_pag", clear_on_submit=True):
            nome_sel = st.selectbox("Aluno", list(opcoes.keys()))
            valor = st.number_input("Valor (R$)", min_value=0.0, step=10.0, format="%.2f")
            data_pag = st.date_input("Data", value=date.today())
            status = st.selectbox("Status", ["pago", "pendente", "cancelado"])
            forma = st.selectbox("Forma", ["Pix", "Dinheiro", "Cartão", "Transferência"])
            obs = st.text_input("Observação", max_chars=200)

            if st.form_submit_button("💾 Registrar", use_container_width=True):
                try:
                    execute_query(_Q_INSERIR, (opcoes[nome_sel], str(data_pag), float(valor), status, forma, obs.strip()))
                    bump_cache()
                    sucesso(f"Pagamento de R$ {valor:.2f} registrado!")
                except Exception:
                    logger.exception("Erro ao registrar pagamento")
                    erro("Erro ao registrar.")

    with tab2:
        df, page, total_pages = paginated_dataframe(
            query=_Q_HISTORICO + " ORDER BY p.data DESC LIMIT ? OFFSET ?",
            count_query=_Q_COUNT,
            page_size=20, key="pag_page"
        )
        if df.empty:
            st.info("Nenhum pagamento.")
            return
        if "valor" in df.columns:
            df["valor"] = df["valor"].apply(lambda v: f"R$ {v:,.2f}")
        st.dataframe(df, use_container_width=True, hide_index=True)
        renderizar_controles_paginacao(page, total_pages, key="pag_page")
