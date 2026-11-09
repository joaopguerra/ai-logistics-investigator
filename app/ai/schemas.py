
from typing import Literal

from pydantic import BaseModel, Field


class InvestigationAnalysis(BaseModel):
    diagnostico: str = Field(
        description="Diagnóstico objetivo da situação logística do pedido, incluindo casos em que o fluxo ocorreu normalmente."
    )

    causa_provavel: str | None = Field(
        description="Possível causa do problema, quando houver evidências."
    )

    evidencias: list[str] = Field(
        description="Lista de fatos encontrados nos dados fornecidos."
    )

    recomendacao: str = Field(
        description="Ação recomendada com base nas evidências."
    )


class InvestigationResult(InvestigationAnalysis):
    status: Literal[
        "NO_PRAZO",
        "EM_RISCO",
        "ATRASADO",
        "ENTREGUE",
        "ENTREGUE_COM_ATRASO",
        "INDETERMINADO"
    ] = Field(
        description="Situação logística calculada pelas regras de negócio."
    )
