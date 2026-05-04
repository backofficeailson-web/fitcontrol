# src/pages/alunos_page.py (amostra do estilo profissional)
import streamlit as st
import pandas as pd
from src.services.cliente_service import (
    listar_clientes_cache,
    criar_cliente,
    desativar_cliente,
    reativar_cliente,
)
from src.models.dto.cliente_dto import ClienteCreateDTO
from src.ui.feedback import sucesso, erro, aviso

def pagina_alunos():
    st.title("👥 Gestão de Alunos")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["➕ Novo Aluno", "📋 Lista de Alunos"])

    with tab1:
        with st.form("cadastro_aluno"):
            col1, col2 = st.columns(2)
            nome = col1.text_input("Nome completo*")
            telefone = col2.text_input("Telefone")
            col1, col2 = st.columns(2)
            mensalidade = col1.number_input("Mensalidade (R$)", min_value=0.0, step=10.0, value=100.0)
            vencimento = col2.text_input("Dia de vencimento", value="10")
            idade = st.number_input("Idade", 12, 100, 30)
            nivel = st.selectbox("Nível de experiência", [
                "Iniciante", "Básico", "Intermediário", "Avançado", "Elite", "Competitivo"
            ])
            objetivo = st.selectbox("Objetivo", ["Hipertrofia", "Força Máxima", "Potência"])
            
            st.markdown("#### 💪 Testes de Força (1RM)")
            c1, c2, c3 = st.columns(3)
            agach = c1.number_input("Agachamento (kg)", 0.0, 500.0, 80.0)
            sup = c2.number_input("Supino (kg)", 0.0, 500.0, 60.0)
            terra = c3.number_input("Terra (kg)", 0.0, 500.0, 100.0)
            peg_dir = st.number_input("Pegada Direita (kg)", 0.0, 200.0, 40.0)
            peg_esq = st.number_input("Pegada Esquerda (kg)", 0.0, 200.0, 38.0)

            if st.form_submit_button("💾 Salvar Aluno"):
                if not nome.strip():
                    aviso("Nome obrigatório.")
                    return
                dto = ClienteCreateDTO(
                    nome=nome, telefone=telefone, mensalidade=mensalidade,
                    vencimento=vencimento, idade=idade, nivel=nivel, objetivo=objetivo,
                    agachamento_1rm=agach, supino_1rm=sup, terra_1rm=terra,
                    pegada_direita=peg_dir, pegada_esquerda=peg_esq
                )
                criar_cliente(dto)
                sucesso(f"Aluno {nome} cadastrado com sucesso!")

    with tab2:
        clientes = listar_clientes_cache()
        if not clientes:
            aviso("Nenhum aluno encontrado.")
            return
        
        df = pd.DataFrame(clientes)
        st.dataframe(
            df[['id', 'nome', 'telefone', 'mensalidade', 'vencimento', 'nivel', 'objetivo']],
            use_container_width=True
        )
        
        st.markdown("---")
        st.subheader("⚙️ Ações rápidas")
        ids = [c['id'] for c in clientes]
        aluno_id = st.selectbox("Selecione o ID do aluno", ids, format_func=lambda x: f"#{x}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Desativar"):
                desativar_cliente(aluno_id)
                st.rerun()
        with col2:
            if st.button("✅ Reativar"):
                reativar_cliente(aluno_id)
                st.rerun()
