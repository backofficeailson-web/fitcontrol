import streamlit as st
from datetime import datetime
from src.core.database import init_db, execute_query
from src.core.auth import verificar_timeout
from src.ui.layout import aplicar_css, logo_sidebar, rodape
from src.utils.backup import backup_db
from src.pages.login_page import tela_login
from src.pages.dashboard_page import mostrar_dashboard
from src.pages.alunos_page import pagina_alunos
from src.pages.avaliacao_page import pagina_avaliacao_fisica, pagina_avaliacao_postural
from src.pages.fotos_page import pagina_fotos
from src.pages.treino_page import pagina_geracao_treino
from src.pages.pagamentos_page import pagina_pagamentos
from src.pages.pdf_page import pagina_pdf

st.set_page_config(page_title="FitControl", page_icon="🟢", layout="wide")
aplicar_css()

# ============================================
# FORCE ADMIN USER - REMOVER APÓS PRIMEIRO LOGIN
# ============================================
if "db_iniciado" not in st.session_state:
    init_db()
    st.session_state.db_iniciado = True

# Recria o usuário admin sempre (garantia)
admin = execute_query("SELECT id FROM usuarios WHERE username = 'admin'", fetchone=True)
if admin:
    execute_query("DELETE FROM usuarios WHERE username = 'admin'")
execute_query(
    "INSERT INTO usuarios (username, senha_hash, nome) VALUES (?, ?, ?)",
    ('admin', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Administrador')
)
# ============================================

if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    tela_login()
    st.stop()

st.session_state.ultima_atividade = datetime.now()
verificar_timeout()

hoje = datetime.now().strftime("%Y-%m-%d")
if st.session_state.get("ultimo_backup") != hoje:
    backup_db()
    st.session_state.ultimo_backup = hoje

logo_sidebar()
menu = st.sidebar.radio("📋 MENU", [
    "Dashboard", "Alunos", "Avaliação Física", "Avaliação Postural",
    "Fotos", "Treino", "Pagamentos", "Relatório PDF"
])

paginas = {
    "Dashboard": mostrar_dashboard,
    "Alunos": pagina_alunos,
    "Avaliação Física": pagina_avaliacao_fisica,
    "Avaliação Postural": pagina_avaliacao_postural,
    "Fotos": pagina_fotos,
    "Treino": pagina_geracao_treino,
    "Pagamentos": pagina_pagamentos,
    "Relatório PDF": pagina_pdf,
}
paginas[menu]()

if st.sidebar.button("🚪 Logout"):
    from src.core.auth import logout
    logout()

rodape()
