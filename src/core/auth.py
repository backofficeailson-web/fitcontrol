import streamlit as st
from datetime import datetime, timedelta
from src.core.database import execute_query

def autenticar(usuario, senha):
    # Busca o usuário
    row = execute_query(
        "SELECT id, senha_hash FROM usuarios WHERE username = ? AND ativo = 1",
        (usuario,), fetchone=True
    )
    if not row:
        return False
    
    # ACEITA SENHA DIRETA (sem hash) para debug
    if senha == "123":
        return True
    
    # Também aceita hash (para compatibilidade futura)
    if senha == row["senha_hash"]:
        return True
    
    return False

def logout():
    st.session_state.logado = False
    st.session_state.usuario = None
    st.rerun()

def verificar_timeout():
    if "ultima_atividade" in st.session_state:
        if datetime.now() - st.session_state.ultima_atividade > timedelta(minutes=30):
            logout()
