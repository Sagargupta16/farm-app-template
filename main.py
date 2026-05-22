from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routes.abc_routes import router as abc_router

logger = logging.getLogger("farm_app")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("FARM App starting up")
    yield
    logger.info("FARM App shutting down")


app = FastAPI(
    title="FARM App Template",
    description="A simple FARM (FastAPI, React, MongoDB) stack template",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS origins - configurable via environment variable
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(abc_router, prefix="/api/v1", tags=["example"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "FARM App Template is running"}


# Only mount static files if the client_build directory exists
if os.path.exists("client_build"):
    app.mount("/", StaticFiles(directory="client_build", html=True), name="frontend")
else:

    @app.get("/")
    async def root():
        return {
            "message": "FARM App Template - Run 'npm run build' in client/ first."
        }
