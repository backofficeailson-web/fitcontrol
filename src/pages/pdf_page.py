import streamlit as st
from fpdf import FPDF
from datetime import date
from src.core.database import execute_query
from src.services.cliente_service import listar_clientes_select_cache, buscar_cliente_cache
from src.ui.feedback import sucesso, erro, aviso
import os, logging

logger = logging.getLogger(__name__)

class RelatorioPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, "AILSON PERSONAL TRAINNER", align="C")
        self.ln(4)
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Relatório gerado em {date.today().strftime('%d/%m/%Y')} - Página " + str(self.page_no()), align="C")

def pagina_pdf():
    st.title("📄 Gerar Relatório PDF")
    clientes = listar_clientes_select_cache()
    if not clientes:
        aviso("Nenhum aluno ativo.")
        return
    opcoes = {c["nome"]: c["id"] for c in clientes}
    nome_sel = st.selectbox("Aluno", list(opcoes.keys()))
    cliente_id = opcoes[nome_sel]
    cliente = buscar_cliente_cache(cliente_id)

    if st.button("📥 Gerar PDF", use_container_width=True):
        av = execute_query(
            "SELECT data, peso, altura, cintura, abdomen, quadril, braco_direito, coxa_direita, observacoes FROM avaliacao_fisica WHERE cliente_id = ? ORDER BY data DESC LIMIT 1",
            (cliente_id,), fetchone=True)
        if not av:
            erro("Nenhuma avaliação física encontrada.")
            return

        pdf = RelatorioPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 12, f"Avaliação Física - {nome_sel}", align="C")
        pdf.ln(6)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 8, f"Idade: {cliente.get('idade','')} anos | Objetivo: {cliente.get('objetivo','')}", align="C")
        pdf.ln(10)

        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "Medidas Corporais", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 7, f"Peso: {av['peso']} kg | Altura: {av['altura']} m")
        pdf.cell(0, 7, f"Cintura: {av['cintura']} cm | Abdômen: {av['abdomen']} cm | Quadril: {av['quadril']} cm")
        pdf.cell(0, 7, f"Braço Dir: {av['braco_direito']} cm | Coxa Dir: {av['coxa_direita']} cm")
        if av.get('observacoes'):
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, "Observações", ln=True)
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 6, av['observacoes'])

        nome_arquivo = f"avaliacao_{nome_sel.replace(' ','_')}_{date.today()}.pdf"
        pdf.output(nome_arquivo)
        with open(nome_arquivo, "rb") as f:
            st.download_button("📥 Baixar PDF", data=f, file_name=nome_arquivo, mime="application/pdf")
        try:
            os.remove(nome_arquivo)
        except:
            pass
        sucesso("PDF gerado com sucesso!")
