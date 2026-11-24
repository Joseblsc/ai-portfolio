# AI Portfolio — Jose Blasco

**AI Engineer & Data Scientist** portfolio showcasing end-to-end machine learning, data engineering, and LLM/agentic workflows built with a standardized Python 3.12 + `uv` architecture and served via FastAPI.

## Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Language & Packaging** | Python 3.12, `uv`, `hatchling` (`src/` layout) |
| **API & Configuration** | FastAPI, Uvicorn, Pydantic v2, `pydantic-settings`, `httpx` |
| **Data & Machine Learning** | Polars, Pandas, NumPy, PyArrow, scikit-learn, SciPy, Matplotlib, Seaborn |
| **AI Engineering** | LangChain, LangChain Core, LangGraph (plus optional `providers` extras) |
| **Quality & Testing** | Pytest, Ruff (lint & format), Mypy (strict function typing) |

## Repository Structure

```text
ai-portfolio/
├── AGENTS.md                        # Agent rules, commands & conventions
├── README.md                        # Portfolio overview, stack, quickstart & project index
├── pyproject.toml                   # Python 3.12 + uv + DS/AI/FastAPI + ruff/mypy/pytest
├── .python-version
├── .env.example
├── .agents/
│   └── skills/
│       └── scaffold-project/SKILL.md
├── docs/
│   └── ARCHITECTURE.md              # Schema & architectural decisions
├── src/ai_portfolio/
│   ├── config.py                    # Settings loaded from env / .env
│   ├── utils/                       # Logging and Step/Pipeline base classes
│   ├── api/
│   │   └── main.py                  # FastAPI app, /health & project routers
│   └── projects/                    # Modular DS & AI projects
└── tests/
    ├── conftest.py
    ├── test_api.py
    └── test_pipelines.py
```

## Quickstart

### 1. Install dependencies

```bash
# Core stack + dev tools (pytest, ruff, mypy)
uv sync --group dev

# Optional: LLM provider integrations (OpenAI, Anthropic, Google GenAI, Community)
uv sync --group dev --extra providers

# Optional: JupyterLab & ipykernel for exploratory notebooks
uv sync --group dev --extra notebooks
```

### 2. Configure environment

Copy `.env.example` to `.env` and fill in any API keys required by LLM projects:

```bash
cp .env.example .env
```

### 3. Run the FastAPI server

```bash
uv run uvicorn ai_portfolio.api.main:app --reload
```

Interactive OpenAPI docs are available at `http://127.0.0.1:8000/docs` and the liveness probe is at `GET /health`.

### 4. Run tests and quality checks

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src tests
```

## Portfolio Projects

| Project | Domain | Pipeline / Stack | API Prefix | Status |
| :--- | :--- | :--- | :--- | :--- |
| _Coming soon_ | — | — | — | — |

## Documentation

- [AGENTS.md](AGENTS.md) — Agent operating instructions and workflow conventions
- [Architecture & Key Decisions](docs/ARCHITECTURE.md) — System schema, stack rationale, and design decisions
