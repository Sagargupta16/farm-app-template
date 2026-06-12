# FARM Stack Template

A clean template for building full-stack applications using the FARM stack:
- **F**astAPI (Python backend)
- **R**eact (Frontend, built with Vite)
- **M**ongoDB (Database)

## Features

- FastAPI backend with automatic API documentation
- React 19 frontend with Vite for fast builds
- MongoDB integration with Motor (async driver)
- Docker and Docker Compose support with healthchecks
- Example CRUD operations (Users)
- CI/CD with GitHub Actions (lint, test, Docker build)
- Ruff for Python linting and formatting
- Environment variable configuration with python-dotenv

## Quick Start

### Prerequisites

- Python 3.13+
- Node.js 22+
- MongoDB (or use Docker)

### Method 1: Using Docker (Recommended)

```bash
git clone <your-repo-url>
cd farm-app-template

# Copy environment config
cp .env.example .env

# Start all services
make docker-up
# or: docker compose up -d
```

- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Method 2: Manual Setup

```bash
# Install all dependencies
make install
# or manually:
pip install -r requirements.txt
# or: uv sync --extra dev
cd client && npm install && cd ..

# Start MongoDB (locally or update config/secrets.yml)

# Run backend (terminal 1)
make dev
# or: uvicorn main:app --reload

# Run frontend (terminal 2)
make dev-frontend
# or: cd client && npm run dev
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173

## Project Structure

```
farm-app-template/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Project metadata and tool config
├── Makefile                # Common dev commands
├── docker-compose.yml      # Docker services
├── Dockerfile              # Backend container
├── .env.example            # Environment variables template
│
├── config/
│   ├── secrets.yml         # MongoDB config (fallback)
│   ├── secrets_parser.py   # Config parser with env var support
│   ├── logging.py          # Logging setup
│   └── logging.yml         # Logging configuration
│
├── models/
│   └── abc_models.py       # Pydantic models
│
├── routes/
│   └── abc_routes.py       # API route handlers
│
├── services/
│   └── abc_services.py     # Business logic layer
│
├── utils/
│   └── hashing.py          # Password hashing utilities
│
├── client/                 # React frontend (Vite)
│   ├── vite.config.js      # Vite configuration
│   ├── eslint.config.js    # ESLint flat config
│   ├── index.html          # HTML entry point
│   ├── package.json
│   └── src/
│       ├── main.jsx        # React entry point
│       ├── App.jsx         # Main component
│       └── App.css         # Styles
│
└── tests/
    └── abc_test.py         # Test files
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and modify as needed:

```bash
cp .env.example .env
```

Environment variables take precedence over `config/secrets.yml`.

### Database Configuration

Via environment variables (preferred):
```
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DATABASE=farm_template
```

Or edit `config/secrets.yml` as a fallback.

## API Documentation

Once the backend is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/users` | Get all users |
| POST | `/api/v1/users` | Create a new user |
| GET | `/api/v1/users/{id}` | Get user by ID |
| DELETE | `/api/v1/users/{id}` | Delete user |

## Available Commands

Run `make help` to see all commands:

```
build                Build frontend for production
clean                Remove build artifacts and caches
dev                  Start backend dev server
dev-frontend         Start frontend dev server
docker-down          Stop all Docker Compose services
docker-logs          Follow Docker Compose logs
docker-rebuild       Rebuild and start all services
docker-up            Start all services with Docker Compose
format               Format Python code with ruff
install              Install all dependencies (backend + frontend)
lint                 Run ruff linter
lint-fix             Run ruff linter with auto-fix
test                 Run backend tests
```

## Adding New Features

1. Add a model in `models/` (e.g., `product_models.py`)
2. Create service logic in `services/` (e.g., `product_services.py`)
3. Add API routes in `routes/` (e.g., `product_routes.py`)
4. Include the router in `main.py`
5. Update the frontend in `client/src/`

## License

MIT License - see the [LICENSE](LICENSE) file for details.
