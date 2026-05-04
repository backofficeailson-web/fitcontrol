import sqlite3
import logging
from src.core.config import DB_PATH, ADMIN_USUARIO, ADMIN_SENHA_HASH

logger = logging.getLogger(__name__)

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn

def execute_query(query, params=(), fetch=False, fetchone=False):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch:
                return [dict(row) for row in cursor.fetchall()]
            if fetchone:
                row = cursor.fetchone()
                return dict(row) if row else None
            conn.commit()
            return cursor.lastrowid
    except sqlite3.Error as e:
        logger.exception("Erro ao executar query: %s | params: %s", query, params)
        raise

def init_db():
    queries = [
        '''CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            nome TEXT,
            ativo INTEGER DEFAULT 1
        )''',
        '''CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT,
            mensalidade REAL,
            vencimento TEXT,
            idade INTEGER,
            nivel TEXT,
            objetivo TEXT,
            agachamento_1rm REAL,
            supino_1rm REAL,
            terra_1rm REAL,
            pegada_direita REAL,
            pegada_esquerda REAL,
            historico TEXT,
            ativo INTEGER DEFAULT 1
        )''',
        '''CREATE TABLE IF NOT EXISTS pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            data TEXT,
            valor REAL,
            status TEXT,
            forma TEXT,
            observacao TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )''',
        '''CREATE TABLE IF NOT EXISTS avaliacao_fisica (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            data TEXT,
            peso REAL,
            altura REAL,
            torax REAL,
            cintura REAL,
            abdomen REAL,
            quadril REAL,
            braco_direito REAL,
            braco_esquerdo REAL,
            coxa_direita REAL,
            coxa_esquerda REAL,
            panturrilha_direita REAL,
            panturrilha_esquerda REAL,
            triceps REAL,
            subescapular REAL,
            peitoral REAL,
            axilar_media REAL,
            suprailiaca REAL,
            abdominal REAL,
            coxa REAL,
            biceps REAL,
            perna REAL,
            observacoes TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )''',
        '''CREATE TABLE IF NOT EXISTS avaliacao_postural (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            data TEXT,
            vista_anterior TEXT,
            vista_posterior TEXT,
            vista_lateral_direita TEXT,
            vista_lateral_esquerda TEXT,
            cabeca TEXT,
            ombros TEXT,
            coluna TEXT,
            quadril TEXT,
            joelhos TEXT,
            pes TEXT,
            observacoes TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )''',
        '''CREATE TABLE IF NOT EXISTS fotos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            data TEXT,
            tipo TEXT,
            foto_path TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )'''
    ]
    try:
        with get_connection() as conn:
            for q in queries:
                conn.execute(q)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_clientes_ativo ON clientes(ativo)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_pagamentos_cliente ON pagamentos(cliente_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_pagamentos_data ON pagamentos(data)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_avaliacao_cliente_data ON avaliacao_fisica(cliente_id, data)")
            conn.commit()
        admin = execute_query("SELECT id FROM usuarios WHERE username = ?", (ADMIN_USUARIO,), fetchone=True)
        if not admin:
            execute_query("INSERT INTO usuarios (username, senha_hash, nome) VALUES (?, ?, ?)",
                          (ADMIN_USUARIO, ADMIN_SENHA_HASH, "Administrador"))
            logger.info("Usuário admin criado.")
    except sqlite3.Error:
        logger.exception("Falha ao inicializar banco de dados.")
        raise
        # Tabela para reset de senha
        conn.execute('''CREATE TABLE IF NOT EXISTS password_resets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            token TEXT NOT NULL UNIQUE,
            expires_at TIMESTAMP NOT NULL,
            used INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
