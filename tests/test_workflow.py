from datetime import datetime, timezone

from app.ai.schemas import InvestigationAnalysis
from app.graph.workflow import build_investigation_graph
from app.models import Order


def test_workflow_executes_delayed_order(monkeypatch):
    order = Order(
        id="98765",
        status="IN_TRANSIT",
        expected_delivery=datetime(2026, 1, 1, tzinfo=timezone.utc),
        events=[]
    )

    analysis = InvestigationAnalysis(
        diagnostico="Pedido atrasado.",
        causa_provavel=None,
        evidencias=["Prazo de entrega ultrapassado."],
        recomendacao="Verificar a situação com a transportadora."
    )

    def fake_analyze_order_node(state):
        assert "atraso" in state["analysis_focus"].lower()
        return {"analysis": analysis}

    monkeypatch.setattr(
        "app.graph.workflow.analyze_order_node",
        fake_analyze_order_node
    )

    graph = build_investigation_graph()

    result = graph.invoke({
        "order": order,
        "question": "Por que meu pedido está atrasado?",
        "current_time": datetime(2026, 1, 2, tzinfo=timezone.utc)
    })

    assert result["status"] == "ATRASADO"
    assert result["result"].status == "ATRASADO"
    assert result["result"].diagnostico == "Pedido atrasado."