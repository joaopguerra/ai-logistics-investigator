
from typing import NotRequired, TypedDict, cast

import pytest
from langgraph.graph import END, START, StateGraph

from app.graph.nodes import route_investigation
from app.graph.state import InvestigationState


class RoutingTestState(TypedDict):
    status: str
    destination: NotRequired[str]


def route_node(state: RoutingTestState) -> dict:
    return {}


def investigate_delay(state: RoutingTestState) -> dict:
    return {"destination": "investigate_delay"}


def analyze_normal_flow(state: RoutingTestState) -> dict:
    return {"destination": "analyze_normal_flow"}


def analyze_other_status(state: RoutingTestState) -> dict:
    return {"destination": "analyze_other_status"}


def route_test(state: RoutingTestState) -> str:
    return route_investigation(cast(InvestigationState, state))


def build_test_graph():
    graph = StateGraph(RoutingTestState)

    graph.add_node("route", route_node)
    graph.add_node("investigate_delay", investigate_delay)
    graph.add_node("analyze_normal_flow", analyze_normal_flow)
    graph.add_node("analyze_other_status", analyze_other_status)

    graph.add_edge(START, "route")

    graph.add_conditional_edges(
        "route",
        route_test,
        {
            "investigate_delay": "investigate_delay",
            "analyze_normal_flow": "analyze_normal_flow",
            "analyze_other_status": "analyze_other_status"
        }
    )

    graph.add_edge("investigate_delay", END)
    graph.add_edge("analyze_normal_flow", END)
    graph.add_edge("analyze_other_status", END)

    return graph.compile()


@pytest.mark.parametrize(
    "status, expected_destination",
    [
        ("ATRASADO", "investigate_delay"),
        ("NO_PRAZO", "analyze_normal_flow"),
        ("EM_RISCO", "analyze_normal_flow"),
        ("ENTREGUE", "analyze_other_status"),
        ("INDETERMINADO", "analyze_other_status"),
    ]
)
def test_graph_routes_by_order_status(status, expected_destination):
    graph = build_test_graph()

    result = graph.invoke({"status": status})

    assert result["destination"] == expected_destination
