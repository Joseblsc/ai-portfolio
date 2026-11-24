# AGENTS.md — AI Portfolio Engineering Guide

This repository is the AI Engineer & Data Scientist portfolio of Jose Blasco. It uses a standard Python 3.12 `src/` layout managed with `uv`, modular `Step` + `Pipeline` orchestration, shared utilities, and a FastAPI serving layer.

## Tech Stack

- **Python**: `3.12` (`.python-version`)
- **Package & Environment Manager**: `uv` (`pyproject.toml`, `uv.lock`, `hatchling`)
- **API & Config**: FastAPI + Uvicorn + Pydantic v2 + `pydantic-settings`
- **Data Science & ML**: NumPy, Pandas, Polars, PyArrow, scikit-learn, SciPy, Matplotlib, Seaborn
- **AI Engineering**: LangChain, LangChain Core, LangGraph (optional LLM provider extras in `providers`)
- **Quality & Testing**: Ruff, Mypy, Pytest

## Repository Schema

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
│   └── ARCHITECTURE.md              # System schema & architectural decisions
├── src/ai_portfolio/
│   ├── config.py                    # Global pydantic-settings configuration
│   ├── api/
│   │   └── main.py                  # FastAPI app factory, /health, & project routers
│   ├── utils/                       # Shared logging and Step/Pipeline base classes
│   └── projects/                    # Individual portfolio projects (<project>/...)
└── tests/
    ├── conftest.py
    ├── test_api.py
    └── test_pipelines.py
```

## Standard Commands

```bash
# Install core + dev dependencies
uv sync --group dev

# Install optional LLM providers or Jupyter notebooks
uv sync --group dev --extra providers
uv sync --group dev --extra notebooks

# Run tests, lint, format check, and type check
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src tests

# Start FastAPI development server
uv run uvicorn ai_portfolio.api.main:app --reload
```

## Engineering & Architecture Rules

1. **Always use `uv`**: Never invoke raw `pip` or global Python. Add dependencies via `uv add` or `pyproject.toml` (keeping vendor LLM SDKs in `[project.optional-dependencies].providers` and Jupyter in `notebooks`) and keep `uv.lock` up to date.
2. **Strict Python 3.12 typing**: Use native typing (`list[str]`, `X | None`, `class Step[InputT, OutputT](ABC)`), `pathlib.Path` for paths, and full parameter/return annotations in `src/` and `tests/` (`mypy` enforces `disallow_untyped_defs = true`).
3. **Composable project layout**: Each project lives under `src/ai_portfolio/projects/<project_name>/` with `config.py`, `schemas.py`, `steps/` (atomic `Step` subclasses), `pipelines/` (builder functions returning `Pipeline`), `router.py` (`/api/v1/<project_slug>` mounted in `api/main.py`), and `README.md`.
4. **Data & libraries**: Prefer **Polars** + Parquet for fast tabular transforms and bridge to **Pandas**/**NumPy** for `scikit-learn` or `seaborn`/`matplotlib`. Keep shared helpers in `src/ai_portfolio/utils/`.
5. **No secrets or raw data in git**: Secrets belong in `.env` (documented in `.env.example`), local datasets in `data/` (gitignored), and model weights/indexes in `artifacts/` (gitignored).
6. **Tests & documentation**: Add unit and FastAPI `TestClient` tests in `tests/` (mocking external LLM/network calls), and document any structural or stack changes in `docs/ARCHITECTURE.md`.

## Further Guidance

- `.agents/skills/scaffold-project/SKILL.md` — Procedure for creating a new portfolio project
- `docs/ARCHITECTURE.md` — Full architecture specification and recorded key decisions
