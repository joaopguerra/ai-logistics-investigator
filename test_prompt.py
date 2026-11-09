
from app.ai.llm import get_chat_model
from app.ai.prompts import investigation_prompt
from app.ai.schemas import InvestigationResult


model = get_chat_model()

structured_model = model.with_structured_output(
    InvestigationResult
)

chain = investigation_prompt | structured_model

response = chain.invoke({
    "order_id": "98765",
    "question": "Por que meu pedido está atrasado?",
    "order_data": """
    Status: Em transporte
    Previsão de entrega: 06/11/2026
    """,
    "tracking_events": """
    05/11/2026 08:00 - Pedido saiu para transferência.
    05/11/2026 18:00 - Transferência não concluída.
    """
})

print(response.model_dump_json(indent=2))