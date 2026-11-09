from langchain_core.prompts import ChatPromptTemplate


investigation_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Você é um analista especializado em operações logísticas.

        Sua responsabilidade é analisar pedidos e eventos de rastreamento.

        Regras:
        - Utilize somente as evidências fornecidas.
        - Nunca invente eventos ou informações.
        - Diferencie fatos de hipóteses.
        - Se não houver informações suficientes, informe isso claramente.
        - Responda em português, de forma objetiva.
        """
    ),
    (
        "human",
        """
        ID do pedido: {order_id}

        Pergunta: {question}

        Dados do pedido:
        {order_data}

        Eventos de rastreamento:
        {tracking_events}

        Analise as informações e responda à pergunta.
        """
    )
])