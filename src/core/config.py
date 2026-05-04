import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "fitcontrol.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Tema Dark Minimalista
PRIMARY = "#6B7280"         # Cinza médio
PRIMARY_LIGHT = "#9CA3AF"   # Cinza claro
BG_DARK = "#111111"         # Fundo preto puro
BG_CARD = "#1A1A1A"         # Cards
TEXT_PRIMARY = "#E5E7EB"    # Texto principal
TEXT_SECONDARY = "#9CA3AF"  # Texto secundário
ACCENT = "#22D3EE"          # Ciano (destaques)
SUCCESS = "#4ADE80"         # Verde sucesso
WARNING = "#FBBF24"         # Amarelo alerta
DANGER = "#F87171"          # Vermelho erro
BORDER = "#2D2D2D"          # Bordas sutis

# Admin
ADMIN_USUARIO = "admin"
ADMIN_SENHA_HASH = "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"

# Upload
MAX_UPLOAD_SIZE = 5 * 1024 * 1024
ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP"}
