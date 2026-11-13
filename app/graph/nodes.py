from app.ai.llm import get_chat_model
from app.ai.prompts import investigation_prompt
from app.ai.schemas import InvestigationAnalysis, InvestigationResult
from app.graph.state import InvestigationState
from app.services.order_status import get_order_status


def classify_order_node(
    state: InvestigationState
) -> dict[str, str]:
    status = get_order_status(
        state["order"],
        state["current_time"]
    )

    return {
        "status": status
    }


def analyze_order_node(
    state: InvestigationState
) -> dict[str, InvestigationAnalysis]:

    order = state["order"]

    order_data = f"""
    Status original: {order.status}
    Status calculado: {state["status"]}
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
        "question": state["question"],
        "order_data": order_data,
        "tracking_events": tracking_events,
        "analysis_focus": state["analysis_focus"]
    })

    return {
        "analysis": analysis
    }


def build_result_node(
    state: InvestigationState
) -> dict[str, InvestigationResult]:

    result = InvestigationResult(
        status=state["status"],
        **state["analysis"].model_dump()
    )

    return {
        "result": result
    }


def route_investigation(
    state: InvestigationState
) -> str:

    status = state["status"]

    if status == "ATRASADO":
        return "investigate_delay"

    if status in ("NO_PRAZO", "EM_RISCO"):
        return "analyze_normal_flow"

    return "analyze_other_status"


def investigate_delay_node(
    state: InvestigationState
) -> dict[str, str]:
    return {
        "analysis_focus": (
            "Investigue possíveis causas do atraso, "
            "considerando os eventos e a previsão de entrega."
        )
    }


def analyze_normal_flow_node(
    state: InvestigationState
) -> dict[str, str]:
    return {
        "analysis_focus": (
            "Analise se os eventos do pedido estão seguindo "
            "um fluxo logístico normal e esperado."
        )
    }


def analyze_other_status_node(
    state: InvestigationState
) -> dict[str, str]:
    return {
        "analysis_focus": (
            "Analise a situação do pedido considerando seu status "
            "e as evidências disponíveis. Identifique limitações "
            "ou informações insuficientes."
        )
    }