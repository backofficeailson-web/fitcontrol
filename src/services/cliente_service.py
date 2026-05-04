import streamlit as st
from src.core.state import get_cache_version, bump_cache
from src.core.database import execute_query
from src.models.dto.cliente_dto import ClienteCreateDTO

@st.cache_data(ttl=60, show_spinner=False)
def listar_clientes_cache(cache_version=1):
    return execute_query("SELECT * FROM clientes WHERE ativo = 1 ORDER BY nome", fetch=True)

@st.cache_data(ttl=60, show_spinner=False)
def buscar_cliente_cache(cliente_id, cache_version=1):
    return execute_query("SELECT * FROM clientes WHERE id = ? AND ativo = 1", (cliente_id,), fetchone=True)

@st.cache_data(ttl=300, show_spinner=False)
def listar_clientes_select_cache(cache_version=1):
    return execute_query("SELECT id, nome FROM clientes WHERE ativo = 1 ORDER BY nome", fetch=True)

def criar_cliente(dto: ClienteCreateDTO):
    execute_query("""
        INSERT INTO clientes (nome,telefone,mensalidade,vencimento,idade,nivel,objetivo,
        agachamento_1rm,supino_1rm,terra_1rm,pegada_direita,pegada_esquerda,historico)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (dto.nome, dto.telefone, dto.mensalidade, dto.vencimento, dto.idade,
          dto.nivel, dto.objetivo, dto.agachamento_1rm, dto.supino_1rm, dto.terra_1rm,
          dto.pegada_direita, dto.pegada_esquerda, ""))
    bump_cache()

def desativar_cliente(cliente_id):
    execute_query("UPDATE clientes SET ativo = 0 WHERE id = ?", (cliente_id,))
    bump_cache()

def reativar_cliente(cliente_id):
    execute_query("UPDATE clientes SET ativo = 1 WHERE id = ?", (cliente_id,))
    bump_cache()
