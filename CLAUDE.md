# CLAUDE.md

> This file stacks on top of the workspace root at `C:\Code\GitHub\`:
> - Root [`CLAUDE.md`](../../CLAUDE.md) -- voice, rules, routing map, references, skills, slash commands, conventions.
> - Root [`MEMORY.md`](../../MEMORY.md) -- live facts across repos.
> - Root [`STATUS.md`](../../STATUS.md) -- live PR/CI/security dashboard.
> - [`.claude/resources/`](../../.claude/resources/README.md) -- deep reference for collaboration, workflow, git, OSS, debugging, voice.
>
> Read those first. The guidance below only adds **repo-specific context** -- it does not override anything in the root.

## Project

FARM stack template (FastAPI + React + MongoDB) used to scaffold new full-stack repos in this workspace (via `repo-scaffold` / `templates/` routing). Ships example CRUD (users), Docker Compose, and CI.

## Stack

- **Language**: Python 3.13+ (backend), JavaScript ESM (frontend)
- **Framework**: FastAPI + Motor (async Mongo); React 19 + Vite 6
- **Database**: MongoDB 8 (Docker service `mongodb`)
- **Package manager**: uv (uv.lock present; requirements.txt kept for CI/Docker), npm in `client/`
- **Deploy target**: none -- template only; Docker Compose for local run

## Run

```
make install            # pip + npm install (or: uv sync --extra dev)
make dev                # uvicorn main:app --reload (port 8000)
make dev-frontend       # cd client && npm run dev (port 5173)
make docker-up          # MongoDB + backend via docker compose
make build              # vite build (frontend)
```

## Test

```
make test               # python -m pytest tests/
```

One example file: `tests/abc_test.py`. Lint/format: `make lint`, `make format` (ruff, line-length 120).

## Entry points

- `main.py` -- FastAPI app: CORS, `/health`, mounts `routes/`, serves `client_build/` if present
- `client/src/main.jsx` -- React entry

## Key files

- `routes/abc_routes.py` / `services/abc_services.py` / `models/abc_models.py` -- the route -> service -> model layering every new feature copies
- `config/secrets_parser.py` -- DB config; env vars override `config/secrets.yml`
- `Makefile` -- canonical command list (`make help`)

## Gotchas

- Env vars (`MONGODB_HOST/PORT/DATABASE/USERNAME/PASSWORD`, `CORS_ORIGINS`) take precedence over `config/secrets.yml`. Copy `.env.example` to `.env` first.
- `main.py:51` only mounts the SPA if `client_build/` exists -- run `make build` before expecting `/` to serve the frontend.
- CI (`.github/workflows/main.yml`) runs Python `3.14` while step names still say 3.13; pyproject requires `>=3.13`.
- Two venv dirs exist locally (`venv/`, `.venv/`) -- use `.venv` (uv). Both are gitignored.
- No auth flow built in; `utils/hashing.py` is just a bcrypt helper.

## Repo-specific rules

- This is a scaffolding template: keep code generic (`abc_*` placeholder naming), no app-specific features.
- Keep deps latest (Renovate enabled); template modernization notes live in workspace memory.

## API routes

- `GET /health` -- health check
- `GET|POST /api/v1/users`, `GET|DELETE /api/v1/users/{id}` -- example CRUD
- See OpenAPI at `/docs` when server is running.

## DB schema

- No migrations (MongoDB). Example collection: `users`.

## Routes / Pages

- `/` -- single page (`client/src/App.jsx`), no client-side router.
