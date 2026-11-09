
from typing import Literal

from pydantic import BaseModel, Field


class InvestigationResult(BaseModel):
    status: Literal[
        "NORMAL",
        "EM_RISCO",
        "ATRASADO",
        "INDETERMINADO"
    ] = Field(
        description="Situação identificada na investigação logística."
    )

    problema: str = Field(
        description="Descrição objetiva do problema identificado."
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
