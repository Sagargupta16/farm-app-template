# Changelog

## [2.1.2] - 2026-10-25

- certifi 2026.7.22 -> 2026.10.23 in `uv.lock`, for the emSign root CAs with compromised intermediate CA keys advisory

## [2.1.1] - 2026-10-25

- Client: vite 8.1.6 -> 8.3.5 for the launch-editor advisories (existence-check bypass, `%` escaping and CLI flag handling on Windows)

## [2.1.0] - 2026-10-16

- Move Python tooling to uv: CI, the Dockerfile and `make` targets install with `uv sync --locked` (CI and the Dockerfile also pass `--no-build`, and every CI `uv run` passes `--locked --no-build`); `requirements.txt` is removed and `uv.lock` is the single source of locked versions
- Dev tools move from the `dev` extra to a `dev` dependency group; drop the unused setuptools `[build-system]` that made `uv sync` fail
- Multi-stage Dockerfile: builds the React client and serves it at `/`, installs locked wheels only with uv (`--no-build`) into `/opt/venv`; the Python stages move from Alpine to `python:3.14-slim` because pymongo has no musllinux wheel
- CI: top-level `contents: read` permissions (`build_and_publish.yml` drops its unused `contents: write` and `packages: write`), `ruff format --check`, new `client` job (ESLint + Vite build), Docker build waits on tests and client, then runs the image until its healthcheck reports healthy and checks `/health` and the SPA at `/`
- ESLint extends `js.configs.recommended`; `fetchUsers()` calls in `App.jsx` are awaited or caught
- Delete button colors reach WCAG AA contrast (4.6:1, hover 5.0:1); the 404 responses are documented in the OpenAPI schema

## [2.0.0] - 2026-03-14

- Modernize to 2026 standards: Python 3.13, Node 22
- Pydantic v2, ESLint flat config, Docker with non-root user

## [1.0.0] - 2023-06-20

- Initial FARM stack template (FastAPI + React + MongoDB)
