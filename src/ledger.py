# src/ledger.py
from dataclasses import dataclass, field, asdict
from typing import Literal, Optional

Source = Literal["cv", "interview"]
Classification = Literal["in_scope", "out_of_scope", "ambiguous"]
Verdict = Literal["confirmed", "contradicted", "unverifiable", "ambiguous", "pending"]
VerificationMethod = Literal["reading", "execution"]

@dataclass
class Claim:
    text: str
    source: Source
    classification: Classification
    classification_justification: str
    verdict: Verdict = "pending"
    verification_method: Optional[VerificationMethod] = None
    evidence: Optional[str] = None

@dataclass
class Ledger:
    case_id: str
    claims: list[Claim] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)