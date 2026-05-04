import shutil
from datetime import datetime
from src.core.config import DB_PATH
import logging

logger = logging.getLogger(__name__)

def backup_db():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = f"{DB_PATH}.backup_{timestamp}"
    try:
        shutil.copy2(DB_PATH, destino)
        logger.info("Backup criado: %s", destino)
    except Exception as e:
        logger.error("Falha ao criar backup: %s", e)
