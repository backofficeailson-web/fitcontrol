import streamlit as st
from src.utils.pdf_generator import gerar_pdf_avaliacao_completa
from src.services.cliente_service import listar_clientes_select_cache
from src.ui.feedback import sucesso, erro, aviso
import os

def pagina_pdf():
    st.title("📄 Gerar Relatório PDF Profissional")
    
    clientes = listar_clientes_select_cache()
    if not clientes:
        aviso("Nenhum aluno ativo cadastrado.")
        return

    opcoes = {c["nome"]: c["id"] for c in clientes}
    nome_sel = st.selectbox("Selecionar aluno", list(opcoes.keys()), key="pdf_aluno")
    cliente_id = opcoes[nome_sel]

    st.markdown("---")
    st.markdown("""
    ### 📋 O relatório inclui:
    - 🎨 **Capa personalizada** com nome, idade e objetivo
    - 📏 **Tabela de medidas corporais** com classificação IMC
    - 📐 **Tabela de dobras cutâneas**
    - 📝 **Observações da última avaliação**
    """)

    if st.button("📥 GERAR PDF PROFISSIONAL", use_container_width=True, type="primary"):
        with st.spinner("Gerando relatório profissional..."):
            arquivo = gerar_pdf_avaliacao_completa(cliente_id)

        if arquivo is None:
            erro("Nenhuma avaliação física encontrada para este aluno.")
            return

        with open(arquivo, "rb") as f:
            st.download_button(
                label="📥 BAIXAR PDF",
                data=f,
                file_name=arquivo,
                mime="application/pdf",
                key="download_pdf"
            )

        try:
            os.remove(arquivo)
        except:
            pass

        sucesso("✅ PDF profissional gerado com sucesso!")
