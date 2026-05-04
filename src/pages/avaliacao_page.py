import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from src.core.database import execute_query
from src.core.state import get_cache_version, bump_cache
from src.services.cliente_service import listar_clientes_cache
from src.ui.feedback import sucesso, erro
import logging

logger = logging.getLogger(__name__)

_Q_INSERIR_FISICA = """
    INSERT INTO avaliacao_fisica (
        cliente_id, data, peso, altura,
        torax, cintura, abdomen, quadril,
        braco_direito, braco_esquerdo,
        coxa_direita, coxa_esquerda,
        panturrilha_direita, panturrilha_esquerda,
        triceps, subescapular, peitoral,
        axilar_media, suprailiaca, abdominal,
        coxa, biceps, perna, observacoes
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
"""

_Q_LISTAR_FISICA = """
    SELECT id, data, peso, altura, cintura, abdomen, quadril,
           braco_direito, braco_esquerdo, coxa_direita, coxa_esquerda,
           triceps, subescapular, peitoral, suprailiaca, abdominal, observacoes
    FROM avaliacao_fisica
    WHERE cliente_id = ?
    ORDER BY data DESC
"""

_Q_INSERIR_POSTURAL = """
    INSERT INTO avaliacao_postural (
        cliente_id, data,
        vista_anterior, vista_posterior,
        vista_lateral_direita, vista_lateral_esquerda,
        cabeca, ombros, coluna, quadril, joelhos, pes, observacoes
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
"""

_Q_LISTAR_POSTURAL = """
    SELECT id, data, cabeca, ombros, coluna, quadril, joelhos, pes, observacoes
    FROM avaliacao_postural
    WHERE cliente_id = ?
    ORDER BY data DESC
"""

def _opcoes_clientes(clientes):
    return {f'{c["nome"]} (ID {c["id"]})': c["id"] for c in clientes}

def pagina_avaliacao_fisica():
    st.title("📏 Avaliação Física")
    clientes = listar_clientes_cache(get_cache_version())
    if not clientes:
        st.info("Nenhum aluno ativo cadastrado.")
        return
    opcoes = _opcoes_clientes(clientes)
    label_sel = st.selectbox("Selecionar aluno", list(opcoes.keys()))
    cliente_id = opcoes[label_sel]
    nome = label_sel.split(" (ID")[0]

    aba1, aba2 = st.tabs(["➕ Nova Avaliação", "📈 Histórico & Evolução"])

    with aba1:
        with st.form("form_avf", clear_on_submit=True):
            st.markdown("##### 📅 Dados gerais")
            col1, col2 = st.columns(2)
            data_av = col1.date_input("Data", value=date.today())
            peso = col1.number_input("Peso (kg)", min_value=0.0, step=0.1)
            altura = col2.number_input("Altura (m)", min_value=0.0, max_value=2.5, step=0.01, format="%.2f")
            torax = col2.number_input("Tórax (cm)", min_value=0.0, step=0.5)
            cintura = st.number_input("Cintura (cm)", min_value=0.0, step=0.5)
            abdomen = st.number_input("Abdômen (cm)", min_value=0.0, step=0.5)
            quadril = st.number_input("Quadril (cm)", min_value=0.0, step=0.5)

            st.markdown("##### 💪 Membros")
            c1, c2, c3, c4 = st.columns(4)
            braco_dir = c1.number_input("Braço D (cm)", min_value=0.0, step=0.5)
            braco_esq = c2.number_input("Braço E (cm)", min_value=0.0, step=0.5)
            coxa_dir = c3.number_input("Coxa D (cm)", min_value=0.0, step=0.5)
            coxa_esq = c4.number_input("Coxa E (cm)", min_value=0.0, step=0.5)
            pant_dir = st.number_input("Panturrilha D (cm)", min_value=0.0, step=0.5)
            pant_esq = st.number_input("Panturrilha E (cm)", min_value=0.0, step=0.5)

            st.markdown("##### 📐 Dobras Cutâneas (mm)")
            d1, d2, d3 = st.columns(3)
            triceps = d1.number_input("Tríceps", min_value=0.0, step=0.5)
            subescap = d1.number_input("Subescapular", min_value=0.0, step=0.5)
            peitoral = d2.number_input("Peitoral", min_value=0.0, step=0.5)
            axilar = d2.number_input("Axilar média", min_value=0.0, step=0.5)
            suprailiaca = d3.number_input("Supra-ilíaca", min_value=0.0, step=0.5)
            abdominal = d3.number_input("Abdominal", min_value=0.0, step=0.5)
            coxa_dobra = st.number_input("Coxa (dobra)", min_value=0.0, step=0.5)
            biceps = st.number_input("Bíceps", min_value=0.0, step=0.5)
            perna = st.number_input("Perna", min_value=0.0, step=0.5)
            obs = st.text_area("Observações", max_chars=500)

            if st.form_submit_button("💾 Salvar Avaliação", use_container_width=True):
                try:
                    execute_query(_Q_INSERIR_FISICA, (
                        cliente_id, str(data_av), peso, altura,
                        torax, cintura, abdomen, quadril,
                        braco_dir, braco_esq, coxa_dir, coxa_esq,
                        pant_dir, pant_esq,
                        triceps, subescap, peitoral,
                        axilar, suprailiaca, abdominal,
                        coxa_dobra, biceps, perna, obs.strip()
                    ))
                    bump_cache()
                    sucesso("✅ Avaliação física salva!")
                    st.rerun()
                except Exception:
                    logger.exception("Erro ao salvar avaliação física")
                    erro("Erro ao salvar. Tente novamente.")

    with aba2:
        rows = execute_query(_Q_LISTAR_FISICA, (cliente_id,), fetch=True)
        if not rows:
            st.info("Nenhuma avaliação física registrada.")
            return
        df = pd.DataFrame(rows)
        df["data_fmt"] = pd.to_datetime(df["data"]).dt.strftime("%d/%m/%Y")
        st.dataframe(df[["data_fmt","peso","cintura","abdomen","quadril","braco_direito","coxa_direita"]], use_container_width=True, hide_index=True)

        if len(df) >= 2:
            metrica = st.selectbox("Métrica", ["peso", "cintura", "abdomen", "quadril"], key="metrica_chart")
            df_chart = df.sort_values("data")
            fig = px.line(df_chart, x="data_fmt", y=metrica, markers=True, color_discrete_sequence=["#2ECC40"])
            fig.update_layout(plot_bgcolor="#1E1E1E", paper_bgcolor="#1E1E1E", font_color="#FFFFFF")
            st.plotly_chart(fig, use_container_width=True)

def pagina_avaliacao_postural():
    st.title("🧍 Avaliação Postural")
    clientes = listar_clientes_cache(get_cache_version())
    if not clientes:
        st.info("Nenhum aluno ativo cadastrado.")
        return
    opcoes = _opcoes_clientes(clientes)
    label_sel = st.selectbox("Selecionar aluno", list(opcoes.keys()), key="avp_sel")
    cliente_id = opcoes[label_sel]

    aba1, aba2 = st.tabs(["➕ Nova Avaliação", "📋 Histórico"])

    with aba1:
        with st.form("form_avp", clear_on_submit=True):
            data_av = st.date_input("Data", value=date.today())
            col1, col2 = st.columns(2)
            cabeca = col1.selectbox("Cabeça", ["Normal", "Alterado leve", "Alterado moderado", "Alterado grave"])
            ombros = col2.selectbox("Ombros", ["Normal", "Alterado leve", "Alterado moderado", "Alterado grave"])
            coluna = col1.selectbox("Coluna", ["Normal", "Alterado leve", "Alterado moderado", "Alterado grave"])
            quadril = col2.selectbox("Quadril", ["Normal", "Alterado leve", "Alterado moderado", "Alterado grave"])
            joelhos = col1.selectbox("Joelhos", ["Normal", "Alterado leve", "Alterado moderado", "Alterado grave"])
            pes = col2.selectbox("Pés", ["Normal", "Alterado leve", "Alterado moderado", "Alterado grave"])
            v_ant = st.text_area("Vista anterior", max_chars=300)
            v_post = st.text_area("Vista posterior", max_chars=300)
            v_dir = st.text_area("Vista lateral direita", max_chars=300)
            v_esq = st.text_area("Vista lateral esquerda", max_chars=300)
            obs = st.text_area("Observações gerais", max_chars=500)

            if st.form_submit_button("💾 Salvar Avaliação Postural", use_container_width=True):
                try:
                    execute_query(_Q_INSERIR_POSTURAL, (
                        cliente_id, str(data_av),
                        v_ant.strip(), v_post.strip(), v_dir.strip(), v_esq.strip(),
                        cabeca, ombros, coluna, quadril, joelhos, pes, obs.strip()
                    ))
                    bump_cache()
                    sucesso("✅ Avaliação postural salva!")
                    st.rerun()
                except Exception:
                    logger.exception("Erro ao salvar avaliação postural")
                    erro("Erro ao salvar. Tente novamente.")

    with aba2:
        rows = execute_query(_Q_LISTAR_POSTURAL, (cliente_id,), fetch=True)
        if not rows:
            st.info("Nenhuma avaliação postural registrada.")
            return
        df = pd.DataFrame(rows)
        df["data"] = pd.to_datetime(df["data"]).dt.strftime("%d/%m/%Y")
        st.dataframe(df, use_container_width=True, hide_index=True)
