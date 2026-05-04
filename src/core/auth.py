import streamlit as st
from datetime import datetime, timedelta
from src.core.database import execute_query

def autenticar(usuario, senha):
    # VERIFICAÇÃO SIMPLES E DIRETA
    if usuario == "admin" and senha == "123":
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
