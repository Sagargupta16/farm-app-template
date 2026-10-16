# Contributing to farm-app-template

This repo is a FARM stack starter: FastAPI backend, React frontend built with Vite, MongoDB. Bug reports, fixes, doc corrections and improvements that keep the template minimal and generic are welcome.

## Setup

You need [uv](https://docs.astral.sh/uv/) (it installs Python 3.14 from `.python-version` if missing; the project supports 3.13 or newer), Node.js (`.nvmrc` pins 24), and MongoDB or Docker.

```bash
cp .env.example .env
make install          # uv sync --locked (app + dev group), then npm install in client/
make dev              # backend on http://localhost:8000
make dev-frontend     # frontend on http://localhost:5173
make docker-up        # MongoDB and the backend with docker compose
```

Environment variables override `config/secrets.yml`. If you use the file, copy it from `config/secrets.example.yml`; both `.env` and `config/secrets.yml` are gitignored.

## Before you open a PR

`.github/workflows/main.yml` runs on every pull request, on the Python version in `.python-version` (3.14):

```bash
uv sync --locked --no-build
uv run ruff check .
uv run ruff format --check .
uv run coverage run --source . --omit 'venv/*,tests/*' -m pytest
uv run coverage report --omit='venv/*,tests/*'

cd client
npm ci --ignore-scripts
npm run lint
npm run build
cd ..

docker build --file Dockerfile --tag farm-app-test .
```

The Makefile shortcuts are `make lint` (ruff check and format check), `make test` and `make format`.

## Conventions

- Keep it a template: generic code, `abc_*` placeholder names, no app-specific features.
- New features follow the existing layering: a model in `models/`, logic in `services/`, routes in `routes/`, the router included in `main.py`, and the UI in `client/src/`.
- Tests live in `tests/` (pytest `testpaths`); `tests/abc_test.py` is the example.
- Ruff settings: line length 120, target py313, rules `E F W I UP B SIM` (ignoring `E226` and `E302`), double quotes; `E501` is ignored under `tests/`.
- Python dependencies live in `pyproject.toml` (dev tools in the `dev` dependency group) and are locked in `uv.lock`. Change them with `uv add <pkg>` or `uv add --dev <pkg>`, or edit `pyproject.toml` and run `uv lock`, then commit both files. CI and the `Dockerfile` install with `uv sync --locked`, which fails if the lockfile is out of date.
- Never commit `.env` or `config/secrets.yml`.
- Commit messages follow Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`), with an optional scope such as `fix(deps):`.
- Add a `CHANGELOG.md` entry under a concrete next version, for example `## [2.1.1] - YYYY-MM-DD`, and bump the version in `pyproject.toml` and `.version` to match (then run `uv lock`).
- Fill in the pull request template: description, changes and testing.

## Security issues

Do not report vulnerabilities in public issues. Follow [SECURITY.md](SECURITY.md).

## License

This project is released under the MIT License (see [LICENSE](LICENSE)). By contributing, you agree that your contributions are licensed under it.
