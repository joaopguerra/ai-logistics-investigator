# AI Logistics Investigator Lite

Aplicação experimental de investigação logística baseada em Inteligência Artificial.

O projeto tem como objetivo analisar dados de pedidos e eventos de rastreamento para identificar possíveis problemas, levantar causas prováveis e recomendar ações com base nas evidências disponíveis.

## Objetivo

Desenvolver uma aplicação capaz de receber uma pergunta sobre um pedido, recuperar seus dados logísticos e utilizar um LLM para produzir um diagnóstico estruturado.

O projeto também é um laboratório prático de aprendizado em Python e AI Engineering.

## Tecnologias

- Python
- FastAPI
- Pydantic
- LangChain
- LangGraph (planejado)
- Google Gemini
- Pytest
- JSON

## Arquitetura prevista

1. Receber o identificador do pedido e a pergunta.
2. Consultar os dados do pedido.
3. Recuperar os eventos de rastreamento.
4. Preparar o contexto da investigação.
5. Analisar as evidências com um LLM.
6. Validar o diagnóstico.
7. Retornar uma resposta estruturada.

## Status do desenvolvimento

**Em desenvolvimento.**

Implementado até o momento:

- Estrutura inicial da aplicação Python.
- API REST com FastAPI para consulta de pedidos.
- Modelagem e validação de dados com Pydantic.
- Integração com Google Gemini por meio do LangChain.
- Prompt parametrizado para investigação logística.
- Resposta estruturada utilizando Pydantic.

Próximas etapas:

- Refinar as regras de diagnóstico.
- Implementar validações de negócio.
- Integrar LangGraph para orquestração.
- Ampliar os testes automatizados.

## Dados e segurança

O MVP utiliza dados logísticos simulados em arquivos JSON.

A chave de API deve ser configurada localmente por meio de variável de ambiente. Arquivos `.env` não devem ser versionados.

## Objetivo de longo prazo

Construir um investigador logístico capaz de analisar ocorrências, apresentar evidências e sugerir ações, mantendo a análise fundamentada nos dados disponíveis.
