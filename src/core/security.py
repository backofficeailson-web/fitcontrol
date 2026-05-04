import hashlib

def hash_senha(senha: str) -> str:
    if not senha:
        raise ValueError("Senha não pode ser vazia.")
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(senha: str, hash_armazenado: str) -> bool:
    if not senha or not hash_armazenado:
        return False
    try:
        return hash_senha(senha) == hash_armazenado
    except Exception:
        return False
