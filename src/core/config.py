import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "fitcontrol.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Cores do tema
VERDE_HULK = "#2ECC40"
VERDE_ESCURO = "#0D3B0D"
VERDE_CLARO = "#7CFC00"
ROXO_HULK = "#6A1B9A"
ROXO_ESCURO = "#3D0F5C"
PRETO = "#0A0A0A"
CINZA_ESCURO = "#1E1E1E"
CINZA_MEDIO = "#2D2D2D"
BRANCO = "#FFFFFF"
AMARELO_ALERTA = "#FFD700"
VERMELHO = "#FF4136"

# Admin
ADMIN_USUARIO = "admin"
ADMIN_SENHA_HASH = "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"

# Upload
MAX_UPLOAD_SIZE = 5 * 1024 * 1024
ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP"}
