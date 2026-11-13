from datetime import datetime

from app.ai.schemas import InvestigationResult
from app.graph.workflow import build_investigation_graph
from app.models import Order


def investigate_order(
    order: Order,
    question: str,
    current_time: datetime
) -> InvestigationResult:

    graph = build_investigation_graph()

    result = graph.invoke({
        "order": order,
        "question": question,
        "current_time": current_time
    })

    return result["result"]