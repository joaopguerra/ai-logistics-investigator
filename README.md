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
- Google Gemini
- Pytest
- JSON

**LangGraph está previsto para uma próxima etapa**, quando será utilizado para orquestrar o fluxo de investigação.

## Arquitetura atual

1. A API recebe o identificador do pedido e a pergunta.
2. A aplicação recupera os dados do pedido no arquivo JSON.
3. As regras de negócio calculam o status logístico.
4. Os dados do pedido e os eventos de rastreamento são enviados ao Gemini por meio do LangChain.
5. O modelo analisa as evidências e gera um diagnóstico estruturado.
6. O Pydantic valida a estrutura da resposta.
7. A API retorna o resultado em JSON.

O status logístico é calculado pela aplicação, não pelo LLM. O modelo fica responsável pela análise das evidências e pela elaboração do diagnóstico.

## Funcionalidades implementadas

- API REST para consulta de pedidos.
- Modelagem e validação dos dados com Pydantic.
- Classificação de status: no prazo, em risco, atrasado, entregue, entregue com atraso e indeterminado.
- Integração com Google Gemini por meio do LangChain.
- Prompt orientado à análise baseada exclusivamente nas evidências fornecidas.
- Resposta estruturada com diagnóstico, causa provável, evidências, recomendação e status.
- Tratamento de pedido inexistente com HTTP 404.
- Testes automatizados das regras de negócio.

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

Os testes atuais validam as regras de classificação logística utilizando dados controlados, sem depender de chamadas ao Gemini.

## Dados e limitações do MVP

O projeto utiliza pedidos e eventos de rastreamento simulados em `data/orders.json`.

Ainda não há integração com transportadoras ou sistemas logísticos reais. A integração com LangGraph, persistência de estado e ampliação dos cenários de teste fazem parte das próximas etapas.

## Próximas etapas

- Integrar LangGraph para orquestrar o fluxo de investigação.
- Ampliar os testes automatizados da API e dos cenários de investigação.
- Melhorar logs e tratamento de erros.
- Documentar e evoluir a arquitetura conforme o MVP amadurecer.

---

Projeto desenvolvido para estudo prático de Python, LLMs e AI Engineering em um contexto de logística.
