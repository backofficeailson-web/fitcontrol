from fpdf import FPDF
from datetime import date, datetime
from src.core.database import execute_query
from src.services.cliente_service import buscar_cliente_cache
import os
import logging

logger = logging.getLogger(__name__)

class PDFProfissional(FPDF):
    def __init__(self, nome_aluno):
        super().__init__()
        self.nome_aluno = nome_aluno
        self.data_hoje = date.today().strftime("%d/%m/%Y")

    def header(self):
        # Faixa verde superior
        self.set_fill_color(46, 204, 64)
        self.rect(0, 0, 210, 8, style='F')
        
        self.set_y(4)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(255, 255, 255)
        self.cell(0, 5, "AILSON PERSONAL TRAINNER", align="C")
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_fill_color(30, 30, 30)
        self.rect(0, 282, 210, 15, style='F')
        
        self.set_y(-14)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(124, 252, 0)
        self.cell(70, 5, f"FitControl v1.0", align="L")
        self.cell(70, 5, f"Relatório gerado em {self.data_hoje}", align="C")
        self.cell(70, 5, f"Página {self.page_no()}/{{nb}}", align="R")

    def capa(self, dados_cliente):
        self.add_page()
        self.alias_nb_pages()
        
        # Fundo escuro
        self.set_fill_color(15, 15, 15)
        self.rect(0, 0, 210, 297, style='F')
        
        # Faixa verde
        self.set_fill_color(46, 204, 64)
        self.rect(0, 80, 210, 40, style='F')
        
        # Título
        self.set_y(85)
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, "RELATÓRIO DE AVALIAÇÃO", align="C")
        self.ln(20)
        
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(124, 252, 0)
        self.cell(0, 12, self.nome_aluno.upper(), align="C")
        self.ln(30)
        
        # Informações
        self.set_font("Helvetica", "", 12)
        self.set_text_color(200, 200, 200)
        info_y = 160
        self.set_y(info_y)
        self.cell(0, 8, f"Idade: {dados_cliente.get('idade', 'N/I')} anos", align="C")
        self.ln(10)
        self.cell(0, 8, f"Objetivo: {dados_cliente.get('objetivo', 'N/I')}", align="C")
        self.ln(10)
        self.cell(0, 8, f"Nível: {dados_cliente.get('nivel', 'N/I')}", align="C")
        self.ln(20)
        
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f"Data: {self.data_hoje}", align="C")

    def secao_titulo(self, titulo):
        self.ln(5)
        self.set_fill_color(46, 204, 64)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, f"  {titulo}", fill=True, ln=True)
        self.ln(5)
        self.set_text_color(0, 0, 0)

    def tabela_medidas(self, dados):
        self.secao_titulo("MEDIDAS CORPORAIS")
        
        self.set_font("Helvetica", "B", 10)
        self.set_fill_color(50, 50, 50)
        self.set_text_color(255, 255, 255)
        
        col_widths = [70, 50, 70]
        headers = ["Medida", "Valor", "Classificação"]
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, border=1, fill=True, align="C")
        self.ln()
        
        self.set_font("Helvetica", "", 10)
        medidas = [
            ("Peso", f"{dados.get('peso', '-')} kg", self._classificar_peso(dados.get('peso', 0))),
            ("Altura", f"{dados.get('altura', '-')} m", "-"),
            ("IMC", f"{dados.get('imc', '-')}", self._classificar_imc(dados.get('imc', 0))),
            ("Cintura", f"{dados.get('cintura', '-')} cm", "-"),
            ("Abdômen", f"{dados.get('abdomen', '-')} cm", "-"),
            ("Quadril", f"{dados.get('quadril', '-')} cm", "-"),
            ("Braço Direito", f"{dados.get('braco_direito', '-')} cm", "-"),
            ("Braço Esquerdo", f"{dados.get('braco_esquerdo', '-')} cm", "-"),
            ("Coxa Direita", f"{dados.get('coxa_direita', '-')} cm", "-"),
            ("Coxa Esquerda", f"{dados.get('coxa_esquerda', '-')} cm", "-"),
        ]
        
        for medida, valor, classificacao in medidas:
            self.set_text_color(0, 0, 0)
            if "IMC" in medida:
                self.set_fill_color(230, 255, 230)
            else:
                self.set_fill_color(255, 255, 255)
            
            self.cell(col_widths[0], 7, f"  {medida}", border=1, fill=True)
            self.cell(col_widths[1], 7, valor, border=1, fill=True, align="C")
            self.cell(col_widths[2], 7, classificacao, border=1, fill=True, align="C")
            self.ln()

    def tabela_dobras(self, dados):
        self.ln(5)
        self.secao_titulo("DOBRAS CUTÂNEAS")
        
        self.set_font("Helvetica", "B", 10)
        self.set_fill_color(50, 50, 50)
        self.set_text_color(255, 255, 255)
        
        self.cell(95, 8, "Dobra", border=1, fill=True, align="C")
        self.cell(95, 8, "Valor (mm)", border=1, fill=True, align="C")
        self.ln()
        
        self.set_font("Helvetica", "", 10)
        dobras = [
            ("Tríceps", dados.get('triceps')),
            ("Subescapular", dados.get('subescapular')),
            ("Peitoral", dados.get('peitoral')),
            ("Axilar Média", dados.get('axilar_media')),
            ("Supra-ilíaca", dados.get('suprailiaca')),
            ("Abdominal", dados.get('abdominal')),
            ("Coxa", dados.get('coxa')),
            ("Bíceps", dados.get('biceps')),
            ("Perna", dados.get('perna')),
        ]
        
        for i, (nome, valor) in enumerate(dobras):
            cor = (255, 255, 255) if i % 2 == 0 else (240, 255, 240)
            self.set_fill_color(*cor)
            self.set_text_color(0, 0, 0)
            self.cell(95, 7, f"  {nome}", border=1, fill=True)
            self.cell(95, 7, f"{valor} mm" if valor else "-", border=1, fill=True, align="C")
            self.ln()

    def secao_observacoes(self, texto):
        if texto:
            self.ln(5)
            self.secao_titulo("OBSERVAÇÕES")
            self.set_font("Helvetica", "", 10)
            self.set_text_color(0, 0, 0)
            self.multi_cell(0, 6, texto)

    def _classificar_peso(self, peso):
        if not peso: return "-"
        return "Normal"
    
    def _classificar_imc(self, imc):
        if not imc: return "-"
        if imc < 18.5: return "Abaixo do peso"
        if imc < 25: return "Peso normal"
        if imc < 30: return "Sobrepeso"
        return "Obesidade"


def gerar_pdf_avaliacao_completa(cliente_id):
    cliente = buscar_cliente_cache(cliente_id)
    if not cliente:
        logger.error("Cliente não encontrado: %s", cliente_id)
        return None

    nome_aluno = cliente.get('nome', 'Aluno')

    # Buscar última avaliação
    av = execute_query("""
        SELECT * FROM avaliacao_fisica
        WHERE cliente_id = ?
        ORDER BY data DESC LIMIT 1
    """, (cliente_id,), fetchone=True)

    if not av:
        logger.warning("Nenhuma avaliação encontrada para: %s", cliente_id)
        return None

    # Calcular IMC
    peso = av.get('peso', 0) or 0
    altura = av.get('altura', 0) or 0
    imc = round(peso / (altura ** 2), 1) if altura > 0 else 0

    dados_av = {
        **av,
        'imc': imc
    }

    # Criar PDF
    pdf = PDFProfissional(nome_aluno)
    pdf.capa(cliente)
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    pdf.tabela_medidas(dados_av)
    pdf.tabela_dobras(dados_av)
    pdf.secao_observacoes(av.get('observacoes', ''))

    # Salvar
    nome_arquivo = f"avaliacao_{nome_aluno.replace(' ', '_')}_{date.today()}.pdf"
    pdf.output(nome_arquivo)
    logger.info("PDF gerado: %s", nome_arquivo)

    return nome_arquivo
