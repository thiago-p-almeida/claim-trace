# src/ledger.py
from dataclasses import dataclass, field, asdict
from typing import Literal, Optional

Fonte = Literal["cv", "entrevista"]
Classificacao = Literal["dentro_do_escopo", "fora_do_escopo", "ambigua"]
Veredito = Literal["confirmada", "contradita", "nao_verificavel", "ambigua", "pendente"]
MetodoVerificacao = Literal["leitura", "execucao"]

@dataclass
class Claim:
    texto: str
    fonte: Fonte
    classificacao: Classificacao
    justificativa_classificacao: str
    veredito: Veredito = "pendente"
    metodo_verificacao: Optional[MetodoVerificacao] = None
    evidencia: Optional[str] = None

@dataclass
class Ledger:
    caso_id: str
    claims: list[Claim] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)