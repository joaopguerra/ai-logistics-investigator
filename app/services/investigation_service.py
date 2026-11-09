
from datetime import datetime

from app.ai.llm import get_chat_model
from app.ai.prompts import investigation_prompt
from app.ai.schemas import InvestigationAnalysis, InvestigationResult
from app.models import Order
from app.services.order_status import get_order_status


def investigate_order(
    order: Order,
    question: str,
    current_time: datetime
) -> InvestigationResult:
    status = get_order_status(order, current_time)

    order_data = f"""
    Status original: {order.status}
    Status calculado: {status}
    Previsão de entrega: {order.expected_delivery.isoformat()}
    """

    tracking_events = "\n".join(
        f"{event.timestamp.isoformat()} - {event.description}"
        for event in order.events
    )

    model = get_chat_model()

    structured_model = model.with_structured_output(
        InvestigationAnalysis
    )

    chain = investigation_prompt | structured_model

    analysis = chain.invoke({
        "order_id": order.id,
        "question": question,
        "order_data": order_data,
        "tracking_events": tracking_events
    })

    return InvestigationResult(
        status=status,
        **analysis.model_dump()
    )
