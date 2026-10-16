# Stage 1: build the React client. vite.config.js writes to ../client_build,
# so from WORKDIR /client the bundle lands in /client_build.
FROM node:24-alpine AS client
WORKDIR /client
COPY client/package.json client/package-lock.json ./
RUN npm ci --ignore-scripts
COPY client/ ./
RUN npm run build

# Stage 2: install the locked Python dependencies (no dev group) into /opt/venv,
# wheels only. The Python stages use Debian slim, not Alpine: pymongo publishes
# no musllinux wheel, so on Alpine it would have to be built from source.
FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=0 \
    UV_PROJECT_ENVIRONMENT=/opt/venv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project --no-build

# Stage 3: runtime. The venv sits outside /app so the docker-compose bind mount
# of the source tree does not hide it.
FROM python:3.14-slim
RUN useradd --create-home appuser
WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
# Backend source. Add a COPY line here when you add a new top-level package.
COPY main.py ./
COPY config/ ./config/
COPY models/ ./models/
COPY routes/ ./routes/
COPY services/ ./services/
COPY utils/ ./utils/
COPY --from=client /client_build ./client_build

ENV PATH="/opt/venv/bin:$PATH"
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
