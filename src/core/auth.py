import streamlit as st
from datetime import datetime, timedelta
from src.core.database import execute_query

def autenticar(usuario, senha):
    if usuario == "admin" and senha == "123":
        return True
    return False

def criar_usuario(email, nome, senha):
    """Cria um novo usuário"""
    # Verifica se já existe
    existente = execute_query(
        "SELECT id FROM usuarios WHERE username = ?",
        (email,), fetchone=True
    )
    if existente:
        return False, "Email já cadastrado."
    
    execute_query(
        "INSERT INTO usuarios (username, senha_hash, nome) VALUES (?, ?, ?)",
        (email, senha, nome)
    )
    return True, "Conta criada com sucesso!"

def gerar_token_reset(email):
    """Gera token para reset de senha"""
    import uuid
    token = str(uuid.uuid4())[:8].upper()
    expires = datetime.now() + timedelta(hours=1)
    
    execute_query(
        "INSERT INTO password_resets (email, token, expires_at) VALUES (?, ?, ?)",
        (email, token, expires.strftime("%Y-%m-%d %H:%M:%S"))
    )
    return token

def resetar_senha(token, nova_senha):
    """Reseta senha usando token válido"""
    reset = execute_query(
        "SELECT email, expires_at, used FROM password_resets WHERE token = ?",
        (token,), fetchone=True
    )
    
    if not reset:
        return False, "Token inválido."
    
    if reset['used']:
        return False, "Token já utilizado."
    
    expires = datetime.strptime(reset['expires_at'], "%Y-%m-%d %H:%M:%S")
    if datetime.now() > expires:
        return False, "Token expirado."
    
    execute_query(
        "UPDATE usuarios SET senha_hash = ? WHERE username = ?",
        (nova_senha, reset['email'])
    )
    execute_query(
        "UPDATE password_resets SET used = 1 WHERE token = ?",
        (token,)
    )
    return True, "Senha alterada com sucesso!"

def logout():
    st.session_state.logado = False
    st.session_state.usuario = None
    st.rerun()

def verificar_timeout():
    if "ultima_atividade" in st.session_state:
        if datetime.now() - st.session_state.ultima_atividade > timedelta(minutes=30):
            logout()
