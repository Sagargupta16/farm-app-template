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
- **Framework**: FastAPI + PyMongo Async (`AsyncMongoClient`); React 19 + Vite 8, ESLint 10 flat config
- **Database**: MongoDB 9 (Docker service `mongodb`, image `mongo:9`)
- **Package manager**: uv -- `pyproject.toml` + `uv.lock` are the only Python dependency source (dev tools in the `dev` dependency group, no `[build-system]`, the app runs from source); CI, Docker and `make` all use `uv sync --locked`. npm in `client/`
- **Deploy target**: none -- template only; Docker Compose for local run

## Run

```
make install            # uv sync --locked + npm install in client/
make dev                # uv run uvicorn main:app --reload (port 8000)
make dev-frontend       # cd client && npm run dev (port 5173)
make docker-up          # MongoDB + backend via docker compose
make build              # vite build (frontend)
```

## Test

```
make test               # uv run pytest tests/
```

One example file: `tests/abc_test.py`. Lint/format: `make lint` (ruff check + format check, same as CI), `make format` (ruff, line-length 120). Frontend: `cd client && npm run lint && npm run build`.

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
- CI (`.github/workflows/main.yml`) gets Python from `.python-version` (3.14) through `astral-sh/setup-uv` (SHA-pinned, no major tag exists); pyproject requires `>=3.13`. Jobs: `lint` -> `test`, `client` (ESLint + Vite build), then `docker-build` after both (builds the image, runs it until healthy, curls `/health` and `/`). Top-level `permissions: contents: read`.
- Docker: multi-stage. `node:24-alpine` builds the client into `/client_build`; a `python:3.14-slim` builder copies uv from `ghcr.io/astral-sh/uv:<pinned>` and runs `uv sync --locked --no-dev --no-install-project --no-build` into `/opt/venv`; the `python:3.14-slim` runtime copies the venv, the backend packages and `client_build`, runs as `appuser`. The venv lives outside `/app` so the compose bind mount (`.:/app`) does not hide it; that same mount does hide the image's `client_build`, so compose serves the SPA only after a host `make build`.
- The Python stages are Debian slim, not Alpine, on purpose: pymongo publishes no musllinux wheel, so `--no-build` fails on Alpine, and any `uv sync` without `--no-build` re-opens SonarCloud docker:S8541. A new dependency without a manylinux wheel fails the image build the same way.
- The runtime stage copies backend packages by name (`main.py`, `config/`, `models/`, `routes/`, `services/`, `utils/`), not `COPY . .`; a new top-level package needs its own `COPY` line.
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
