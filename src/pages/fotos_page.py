import streamlit as st
import pandas as pd
from datetime import date
from src.core.database import execute_query
from src.core.config import UPLOAD_DIR, MAX_UPLOAD_SIZE
from src.services.cliente_service import listar_clientes_cache
from src.ui.feedback import sucesso, erro, aviso
from src.ui.form_lock import is_locked, lock, unlock
from PIL import Image, ImageOps
import os, uuid, io
import logging

logger = logging.getLogger(__name__)

Image.MAX_IMAGE_PIXELS = 20_000_000

def _salvar_foto(cliente_id, uploaded_file, tipo):
    try:
        img = Image.open(io.BytesIO(uploaded_file.read()))
        img = ImageOps.exif_transpose(img)
        if img.mode not in ("RGB",):
            img = img.convert("RGB")
        img.thumbnail((1200, 1200))

        aluno_dir = os.path.join(UPLOAD_DIR, str(cliente_id))
        os.makedirs(aluno_dir, exist_ok=True)
        nome_arquivo = f"{tipo}_{uuid.uuid4().hex[:8]}.jpg"
        caminho = os.path.join(aluno_dir, nome_arquivo)
        img.save(caminho, "JPEG", quality=85, optimize=True)
        return caminho
    except Exception as e:
        raise ValueError(f"Erro ao processar imagem: {e}")

def pagina_fotos():
    st.title("📸 Fotos Avaliativas")
    clientes = listar_clientes_cache()
    if not clientes:
        aviso("Nenhum aluno ativo.")
        return

    opcoes = {f'{c["nome"]} (ID {c["id"]})': c["id"] for c in clientes}
    label_sel = st.selectbox("Selecionar aluno", list(opcoes.keys()))
    cliente_id = opcoes[label_sel]

    aba1, aba2 = st.tabs(["📤 Upload", "🖼️ Galeria"])

    with aba1:
        data_foto = st.date_input("Data", value=date.today())
        col1, col2, col3 = st.columns(3)
        with col1:
            frente = st.file_uploader("Frente", type=['jpg','jpeg','png','webp'], key="frente")
            if frente: st.image(frente, width=200)
        with col2:
            costas = st.file_uploader("Costas", type=['jpg','jpeg','png','webp'], key="costas")
            if costas: st.image(costas, width=200)
        with col3:
            perfil = st.file_uploader("Perfil", type=['jpg','jpeg','png','webp'], key="perfil")
            if perfil: st.image(perfil, width=200)

        if st.button("📤 Salvar Fotos", use_container_width=True):
            if is_locked("salvando_fotos"):
                aviso("Aguarde, já está salvando...")
            else:
                lock("salvando_fotos")
                salvo = False
                try:
                    for img, tipo in [(frente, "frente"), (costas, "costas"), (perfil, "perfil")]:
                        if img:
                            try:
                                if img.size > MAX_UPLOAD_SIZE:
                                    erro(f"{tipo}: arquivo muito grande (máx 5MB).")
                                    continue
                                caminho = _salvar_foto(cliente_id, img, tipo)
                                execute_query(
                                    "INSERT INTO fotos (cliente_id, data, tipo, foto_path) VALUES (?,?,?,?)",
                                    (cliente_id, str(data_foto), tipo, caminho))
                                salvo = True
                                sucesso(f"Foto {tipo} salva!")
                            except Exception as e:
                                erro(f"Erro ao salvar {tipo}: {e}")
                    if not salvo:
                        aviso("Nenhuma foto foi enviada.")
                finally:
                    unlock("salvando_fotos")

    with aba2:
        fotos = execute_query("SELECT * FROM fotos WHERE cliente_id=? ORDER BY data DESC, id DESC", (cliente_id,), fetch=True)
        if not fotos:
            st.info("Nenhuma foto.")
            return
        datas = sorted(set(f["data"] for f in fotos), reverse=True)
        for data in datas:
            with st.expander(f"📅 {data}"):
                cols = st.columns(3)
                fotos_data = [f for f in fotos if f["data"] == data]
                for i, f in enumerate(fotos_data):
                    with cols[i % 3]:
                        if os.path.exists(f["foto_path"]):
                            st.image(f["foto_path"], caption=f["tipo"].capitalize(), width=250)
                        else:
                            st.warning("Foto não encontrada")
