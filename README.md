# AI Logistics Investigator Lite

Aplicação experimental de investigação logística que utiliza Inteligência Artificial para analisar pedidos e eventos de rastreamento, identificar situações de risco e produzir diagnósticos estruturados com base nas evidências disponíveis.

O projeto também é um laboratório prático de desenvolvimento com Python e AI Engineering, aplicado a um cenário próximo de operações logísticas reais.

## Objetivo

Receber uma pergunta sobre um pedido, recuperar seus dados logísticos e utilizar um modelo de linguagem para analisar as evidências e retornar:

- Diagnóstico da situação do pedido.
- Possível causa, quando houver evidências.
- Fatos que sustentam a análise.
- Recomendação de ação.
- Status logístico calculado por regras de negócio.

## Tecnologias

- Python 3.12+
- FastAPI
- Pydantic
- LangChain
- LangGraph
- Google Gemini
- Pytest
- JSON

## Arquitetura

A aplicação separa as responsabilidades de regras de negócio, orquestração e análise por Inteligência Artificial.

### Fluxo de investigação

1. A API recebe o identificador do pedido e a pergunta.
2. A aplicação recupera os dados do pedido no arquivo JSON.
3. O LangGraph inicia o workflow de investigação.
4. O nó de classificação calcula o status logístico utilizando regras de negócio em Python.
5. O grafo realiza um roteamento condicional conforme o status:
   - Pedido atrasado: direciona para investigação do atraso.
   - Pedido no prazo ou em risco: direciona para análise do fluxo normal.
   - Outros status: direciona para análise da situação e das informações disponíveis.
6. O nó de análise utiliza LangChain e Google Gemini para interpretar os dados e eventos de rastreamento.
7. O resultado é estruturado e validado com Pydantic.
8. A API retorna o diagnóstico em JSON.

### Decisão arquitetural

O modelo de IA não determina sozinho o status logístico do pedido.

As regras de negócio são implementadas em Python, garantindo maior previsibilidade na classificação. O LLM é responsável por interpretar as evidências, identificar possíveis causas e produzir recomendações.

O LangGraph coordena as etapas e permite que diferentes caminhos de investigação sejam executados conforme a situação do pedido.

## Funcionalidades implementadas

- API REST para consulta de pedidos.
- Modelagem e validação dos dados com Pydantic.
- Classificação de status: no prazo, em risco, atrasado, entregue, entregue com atraso e indeterminado.
- Integração com Google Gemini por meio do LangChain.
- Orquestração do fluxo de investigação com LangGraph.
- Roteamento condicional conforme o status logístico.
- Prompt orientado à análise baseada nas evidências fornecidas.
- Resposta estruturada com diagnóstico, causa provável, evidências, recomendação e status.
- Tratamento de pedido inexistente com HTTP 404.
- Testes automatizados das regras de negócio, roteamento e execução do workflow.

## Como executar o projeto

### Pré-requisitos

- Python 3.12 ou superior.
- Uma chave de API do Google Gemini, obtida no [Google AI Studio](https://aistudio.google.com/app/apikey).

### 1. Clonar o repositório

```bash
git clone https://github.com/joaopguerra/ai-logistics-investigator.git
cd ai-logistics-investigator
```

### 2. Criar e ativar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements-dev.txt
```

### 4. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GOOGLE_API_KEY=sua_chave_do_google_gemini
GOOGLE_GENAI_API_VERSION=v1beta
```

Não compartilhe nem versione sua chave de API. O arquivo `.env` já está incluído no `.gitignore`.

### 5. Executar a API

```bash
fastapi dev app/main.py
```

A documentação interativa estará disponível em:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/health` | Verifica a saúde da aplicação |
| GET | `/orders` | Lista os pedidos disponíveis |
| GET | `/orders/{order_id}` | Consulta um pedido |
| POST | `/orders/{order_id}/investigate` | Investiga um pedido com auxílio do Gemini |

### Exemplo de investigação

Requisição:

```http
POST /orders/98766/investigate
Content-Type: application/json
```

Corpo:

```json
{
  "question": "O pedido foi entregue dentro do prazo?"
}
```

A resposta contém o diagnóstico, a causa provável, as evidências, a recomendação e o status calculado.

## Executar os testes

```bash
python -m pytest -v
```

A suíte atual possui 15 testes automatizados, cobrindo:

- Regras de classificação logística.
- Roteamento condicional do LangGraph.
- Execução do workflow de investigação.

Os testes automatizados utilizam dados controlados e simulação da análise, sem depender de chamadas reais ao Gemini.

## Dados e limitações do MVP

O projeto utiliza pedidos e eventos de rastreamento simulados em `data/orders.json`.

Ainda não há integração com transportadoras ou sistemas logísticos reais. A aplicação também não possui persistência de histórico de investigações ou suporte a múltiplos provedores de LLM.

## Próximas etapas

- Melhorar a resiliência e o tratamento de falhas nas chamadas aos modelos.
- Preparar a arquitetura para suportar diferentes provedores de LLM.
- Ampliar os testes automatizados da API e dos cenários de investigação.
- Adicionar RAG para consulta de documentos e procedimentos logísticos.
- Integrar banco de dados vetorial.
- Implementar observabilidade com LangFuse.
- Evoluir documentação, infraestrutura e qualidade da aplicação.

---

Projeto desenvolvido para estudo prático de Python, LLMs, LangChain, LangGraph e AI Engineering em um contexto de logística.