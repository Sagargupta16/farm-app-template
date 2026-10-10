# Contributing to farm-app-template

This repo is a FARM stack starter: FastAPI backend, React frontend built with Vite, MongoDB. Bug reports, fixes, doc corrections and improvements that keep the template minimal and generic are welcome.

## Setup

You need Python 3.13 or newer (`.python-version` pins 3.14), Node.js (`.nvmrc` pins 24), and MongoDB or Docker.

```bash
cp .env.example .env
make install          # pip install -r requirements.txt, then npm install in client/
make dev              # backend on http://localhost:8000
make dev-frontend     # frontend on http://localhost:5173
make docker-up        # MongoDB and the backend with docker compose
```

Environment variables override `config/secrets.yml`. If you use the file, copy it from `config/secrets.example.yml`; both `.env` and `config/secrets.yml` are gitignored.

## Before you open a PR

`.github/workflows/main.yml` runs on every pull request, on Python 3.14:

```bash
pip install -r requirements.txt ruff
ruff check .
pip install -r requirements.txt coverage
coverage run --source . --omit 'venv/*,tests/*' -m pytest
coverage report --omit='venv/*,tests/*'
docker build --file Dockerfile --tag farm-app-test .
```

The Makefile shortcuts are `make lint`, `make test` and `make format`. If you touch the frontend, also run the ESLint script, which CI does not run:

```bash
cd client
npm run lint
```

## Conventions

- Keep it a template: generic code, `abc_*` placeholder names, no app-specific features.
- New features follow the existing layering: a model in `models/`, logic in `services/`, routes in `routes/`, the router included in `main.py`, and the UI in `client/src/`.
- Tests live in `tests/` (pytest `testpaths`); `tests/abc_test.py` is the example.
- Ruff settings: line length 120, target py313, rules `E F W I UP B SIM` (ignoring `E226` and `E302`), double quotes; `E501` is ignored under `tests/`.
- Python dependencies are listed in both `pyproject.toml` and `requirements.txt`. CI and the `Dockerfile` install from `requirements.txt`, so change both together.
- Never commit `.env` or `config/secrets.yml`.
- Commit messages follow Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`), with an optional scope such as `fix(deps):`.
- Add a `CHANGELOG.md` entry under a concrete next version, for example `## [2.0.1] - YYYY-MM-DD`.
- Fill in the pull request template: description, changes and testing.

## Security issues

Do not report vulnerabilities in public issues. Follow [SECURITY.md](SECURITY.md).

## License

This project is released under the MIT License (see [LICENSE](LICENSE)). By contributing, you agree that your contributions are licensed under it.
