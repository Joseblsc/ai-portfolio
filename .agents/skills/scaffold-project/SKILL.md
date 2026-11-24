---
name: scaffold-project
description: >-
  Scaffold a new AI Engineer or Data Scientist portfolio project under
  `src/ai_portfolio/projects/`, wire its FastAPI router, add tests, and update
  documentation.
---

# Scaffold a New Portfolio Project

Use this skill whenever adding a new project under `src/ai_portfolio/projects/`.

## Inputs Needed

- `project_name`: `snake_case` package name (e.g., `rag_assistant`, `churn_predictor`)
- `route_slug`: `kebab-case` API prefix segment (e.g., `rag-assistant`, `churn-predictor`)
- Brief description of the problem, dataset, steps, and expected API endpoint(s)

## Procedure

1. **Create the project package**:
   - Create `src/ai_portfolio/projects/<project_name>/` with:
     - `__init__.py`
     - `README.md` (Problem Statement, Dataset, Pipeline Architecture, Evaluation Metrics, API Endpoints, Local Usage)
     - `config.py` (Pydantic `BaseModel` hyperparameters and paths)
     - `schemas.py` (Pydantic v2 request/response and step boundary contracts)
     - `steps/` (atomic `Step[InputT, OutputT]` subclasses, or LangChain/LangGraph components wrapped in `Step`s)
     - `pipelines/` (factory function returning `ai_portfolio.utils.pipelines.Pipeline`)
     - `router.py` (`APIRouter(prefix="/api/v1/<route_slug>", tags=["<route_slug>"])`)

2. **Mount the router in FastAPI**:
   - Import and register `<project_name>.router` in `src/ai_portfolio/api/main.py` inside `create_app()`.

3. **Add tests**:
   - Add unit tests for steps and pipelines in `tests/test_<project_name>.py`.
   - Add API endpoint tests in `tests/test_<project_name>_api.py` (or `tests/test_api.py`) using the `client` fixture from `tests/conftest.py`.

4. **Update documentation**:
   - Add the new project row to the Portfolio Projects table in root `README.md`.

5. **Verify**:
   - Run `uv run ruff check . && uv run ruff format --check . && uv run mypy src tests && uv run pytest`.
