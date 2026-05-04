from dataclasses import dataclass

@dataclass
class ClienteCreateDTO:
    nome: str
    telefone: str
    mensalidade: float
    vencimento: str
    idade: int
    nivel: str
    objetivo: str
    agachamento_1rm: float
    supino_1rm: float
    terra_1rm: float
    pegada_direita: float
    pegada_esquerda: float
