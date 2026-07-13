# 🦌 DeerFlow Research Agent

**A long-horizon research agent** inspired by ByteDance's DeerFlow architecture (~70.7k GitHub stars), implementing the **"agents as an organisation" pattern** with sub-agents, persistent memory, and context engineering.

> Part of the [AY Automate](https://github.com/nagarjunak-pixel) AI framework demo series.

## 🏗 Architecture

```
┌────────────────────────────────────────────────────────┐
│                  Research Agent                         │
│                  (Orchestrator)                         │
├────────────┬───────────────┬──────────────┬────────────┤
│  📋 Planner │  🔍 Searcher  │  🧠 Analyzer │  💾 Memory │
│  Decompose  │  Web search   │  Synthesize  │  Context   │
│  into tasks │  & gather     │  & report    │  Store     │
└────────────┴───────────────┴──────────────┴────────────┘
```

## 🚀 Quick Start

```bash
git clone https://github.com/nagarjunak-pixel/deerflow-research-agent.git
cd deerflow-research-agent
pip install -r requirements.txt

# Run research
python research_agent.py "AI regulation trends in India 2026"

# Deep research
python research_agent.py --topic "Telugu tech ecosystem" --depth deep

# Resume a session
python research_agent.py --resume abc12345
```

## 📁 Project Structure

```
deerflow-research-agent/
├── research_agent.py        # Main orchestrator
├── sub_agents/
│   ├── planner.py           # Topic decomposition
│   ├── searcher.py          # Web search (DuckDuckGo)
│   └── analyzer.py          # Synthesis & reporting
├── memory/
│   └── context_store.py     # Persistent session memory
├── docs/                    # Documentation (Netlify)
├── requirements.txt
└── .env.example
```

## 🔗 Related Projects

| Project | Framework | Purpose |
|---------|-----------|---------|
| [LangGraph LocalAI TV](https://github.com/nagarjunak-pixel/langgraph-localai-tv) | LangGraph | Production pipeline |
| [CrewAI Telugu Newsroom](https://github.com/nagarjunak-pixel/crewai-telugu-newsroom) | CrewAI | Multi-agent crew |
| [Firecrawl NEXUS RSS](https://github.com/nagarjunak-pixel/firecrawl-nexus-rss) | Firecrawl | Web scraping |

## 📄 License

MIT License — Built for [Surya Agentic Academy](https://github.com/nagarjunak-pixel)
