# Repository Architecture & Key Decisions

This document captures the structure, stack, and foundational technical decisions for `ai-portfolio`.

## 1. Design Goals

- **Standard Python packaging**: Follow the PEP 517/621 `src/` layout so tests and scripts always import the installed package via `uv` + `hatchling`.
- **Lean, project-first layout**: Keep repository scaffolding minimal so real Data Science and AI Engineering projects remain the focus.
- **Consistent project modularity**: Every project follows one predictable structure (`config.py`, `schemas.py`, `steps/`, `pipelines/`, `router.py`, `README.md`).
- **Unified serving layer**: A single FastAPI application factory mounts `/health` and versioned project routers (`/api/v1/<project>`).

## 2. Source Package Structure (`src/ai_portfolio/`)

- `config.py`: `Settings(BaseSettings)` loads typed configuration from environment variables and `.env` (`app_name`, `environment`, `log_level`, `data_dir`, `artifacts_dir`), exposed via cached `get_settings()`.
- `utils/`: Shared cross-project helpers:
  - `logging.py`: `configure_logging(level)` and `get_logger(name)` with a consistent timestamped format.
  - `pipelines.py`: Generic `Step[InputT, OutputT]` ABC and sequential `Pipeline` runner with per-step timing logs in milliseconds.
- `api/main.py`: `create_app()` configures logging, registers CORS middleware, defines `GET /health`, and mounts project routers. Exports `app` for `uvicorn ai_portfolio.api.main:app`.
- `projects/<project_name>/`: Self-contained portfolio projects containing `config.py`, `schemas.py`, `steps/`, `pipelines/`, `router.py`, and `README.md`.

## 3. Key Architectural Decisions

### Decision 1: Python 3.12, `uv`, and Quality Tooling
- **Choice**: Pin Python 3.12 (`>=3.12,<3.13`) in `.python-version` and `pyproject.toml`; manage environments and lockfiles (`uv.lock`) with `uv`; build with `hatchling`; enforce quality with `ruff` (lint + 100-char formatting), `mypy` (`disallow_untyped_defs = true`), and `pytest`.
- **Rationale**: Combines modern Python 3.12 typing (PEP 695 generics, `X | Y` unions) and broad ML/AI wheel support with fast, deterministic dependency resolution in one tool.

### Decision 2: `src/` Layout & Multi-Project Monorepo Schema
- **Choice**: House all projects under `src/ai_portfolio/projects/<project_name>/`, share cross-cutting primitives in `src/ai_portfolio/utils/`, and ignore local `data/` and `artifacts/` directories in `.gitignore` (created on demand when needed by a project).
- **Rationale**: Prevents import shadowing, avoids duplicating boilerplate across portfolio projects, and keeps large datasets and model weights out of git history without cluttering the repo with empty placeholder folders.

### Decision 3: `Step` + `Pipeline` Abstraction with Pydantic Contracts
- **Choice**: Model workflows as small `Step[InputT, OutputT]` subclasses composed by `Pipeline`, paired with Pydantic v2 `BaseModel` configs and schemas.
- **Rationale**: Keeps `scikit-learn`, `polars`, and `langchain`/`langgraph` logic decoupled from FastAPI, unit-testable in isolation, and consistently instrumented with timing logs.

### Decision 4: FastAPI Serving Layer and Core DS / AI Stack
- **Choice**:
  - **Serving**: Unified FastAPI + Uvicorn entrypoint (`src/ai_portfolio/api/main.py`) with project routers under `/api/v1/<project>`.
  - **Core Data Science**: `numpy`, `pandas`, `polars`, `pyarrow`, `scikit-learn`, `scipy`, `matplotlib`, `seaborn` (Polars for fast tabular transforms; Pandas/NumPy for ML/plotting interoperability).
  - **Core AI Engineering**: `langchain`, `langchain-core`, `langgraph`.
  - **Optional Extras**: Vendor LLM SDKs (`providers`) and Jupyter (`notebooks`) live under `[project.optional-dependencies]` so base installs remain lean and provider-agnostic.

## 4. Quality Gates

All changes must pass:
- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run mypy src tests`
- `uv run pytest`
