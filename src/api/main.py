"""
FastAPI application entry point for the DXC AI Readiness Diagnostic V0.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.routes import submission, review
from src.database import init_db

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Lifespan handler (startup / shutdown)
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    # Startup
    logger.info("DXC AI Readiness Diagnostic — starting up")
    try:
        await init_db()
        logger.info("Database initialised successfully")
    except Exception as exc:
        logger.error(f"Database initialisation failed: {exc}")
        # Don't crash on startup failure — allow health checks to surface the issue
    yield
    # Shutdown
    logger.info("DXC AI Readiness Diagnostic — shutting down")


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------


app = FastAPI(
    title="DXC AI Readiness Diagnostic",
    description=(
        "AI-driven assessment platform that produces personalised AI readiness scorecards "
        "for enterprise prospects. Combines a 16-question adaptive questionnaire with "
        "automated research across financial, news, and technology signals to produce "
        "a composite readiness score across six dimensions."
    ),
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Global exception handler
# ---------------------------------------------------------------------------


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Return a structured error response for unhandled exceptions."""
    logger.exception(f"Unhandled exception on {request.method} {request.url}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred. Please try again or contact support.",
            "detail": str(exc) if app.debug else None,
        },
    )


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------


app.include_router(submission.router)
app.include_router(review.router, prefix="/api/review")


# ---------------------------------------------------------------------------
# Health & info endpoints
# ---------------------------------------------------------------------------


@app.get("/health", tags=["system"])
async def health() -> Dict[str, Any]:
    """Service health check."""
    return {
        "status": "ok",
        "version": "0.1.0",
        "service": "DXC AI Readiness Diagnostic",
    }


@app.get("/", tags=["system"])
async def root() -> Dict[str, Any]:
    """Root endpoint — API info."""
    return {
        "service": "DXC AI Readiness Diagnostic",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
        "submission": {
            "start": "POST /api/submission/start",
            "complete": "POST /api/submission/complete",
            "status": "GET /api/submission/status/{prospect_id}",
            "demo": "GET /api/submission/demo/{scenario}",
        },
        "review": {
            "queue": "GET /api/review/queue",
            "detail": "GET /api/review/{prospect_id}",
            "approve": "POST /api/review/{prospect_id}/approve",
            "adjust": "POST /api/review/{prospect_id}/adjust",
        },
    }
