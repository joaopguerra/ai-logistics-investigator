from datetime import datetime
from typing import NotRequired, TypedDict

from app.ai.schemas import InvestigationAnalysis, InvestigationResult
from app.models import Order


class InvestigationState(TypedDict):
    order: Order
    question: str
    current_time: datetime

    status: NotRequired[str]
    analysis_focus: NotRequired[str]
    analysis: NotRequired[InvestigationAnalysis]
    result: NotRequired[InvestigationResult]
