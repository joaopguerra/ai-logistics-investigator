
from langgraph.graph import END, START, StateGraph

from app.graph.nodes import (
    analyze_normal_flow_node,
    analyze_order_node,
    analyze_other_status_node,
    build_result_node,
    classify_order_node,
    investigate_delay_node,
    route_investigation,
)
from app.graph.state import InvestigationState


def build_investigation_graph():
    graph = StateGraph(InvestigationState)

    graph.add_node("classify_order", classify_order_node)
    graph.add_node("investigate_delay", investigate_delay_node)
    graph.add_node("analyze_normal_flow", analyze_normal_flow_node)
    graph.add_node("analyze_other_status", analyze_other_status_node)
    graph.add_node("analyze_order", analyze_order_node)
    graph.add_node("build_result", build_result_node)

    graph.add_edge(START, "classify_order")

    graph.add_conditional_edges(
        "classify_order",
        route_investigation,
        {
            "investigate_delay": "investigate_delay",
            "analyze_normal_flow": "analyze_normal_flow",
            "analyze_other_status": "analyze_other_status",
        }
    )

    graph.add_edge("investigate_delay", "analyze_order")
    graph.add_edge("analyze_normal_flow", "analyze_order")
    graph.add_edge("analyze_other_status", "analyze_order")

    graph.add_edge("analyze_order", "build_result")
    graph.add_edge("build_result", END)

    return graph.compile()
