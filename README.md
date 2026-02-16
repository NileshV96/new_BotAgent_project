# Chatbot Multi-Agent + MCP Tools (LangChain + LangGraph)

A minimal multi-agent chatbot project using:
- **LangChain** (LLM wrapper)
- **LangGraph** (multi-agent workflow)
- **MCP** (Model Context Protocol) local tool servers (free + open APIs)

## Planned agents
1. Orchestrator (router)
2. Research agent (tool user)
3. Writer agent (final response)

## Planned MCP tools (free/open)
- Wikipedia
- DuckDuckGo Search
- arXiv
- Open-Meteo Weather
- OpenLibrary

## Setup (later steps)
1. Copy `.env.example` to `.env`
2. Add your `OPENAI_API_KEY`
3. Install deps: `pip install -e .`
4. Run tool servers + run chatbot
