"""
Agentic Career Counseling Companion
Main FastAPI Application Entry Point
IBM Cloud / IBM Granite Powered
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
import logging

from config import settings
from database import engine, Base
from routes import auth, students, career, assessment, market

# ── Logging Setup ────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ── Create DB Tables ─────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── FastAPI App ───────────────────────────────────────────────
app = FastAPI(
    title="Agentic Career Counseling Companion",
    description=(
        "An intelligent, autonomous AI agent powered by IBM Granite "
        "that monitors student performance, interests, and real-time "
        "labor market trends to deliver personalized career pathway suggestions."
    ),
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────
app.include_router(auth.router,       prefix="/api/auth",       tags=["Authentication"])
app.include_router(students.router,   prefix="/api/students",   tags=["Student Profile"])
app.include_router(assessment.router, prefix="/api/assessment", tags=["Assessment"])
app.include_router(career.router,     prefix="/api/career",     tags=["Career Guidance"])
app.include_router(market.router,     prefix="/api/market",     tags=["Labor Market"])


@app.get("/", tags=["Health"])
async def root():
    return {
        "service": "Agentic Career Counseling Companion",
        "status": "running",
        "powered_by": "IBM Granite on WatsonX.ai",
        "version": "1.0.0",
    }


@app.get("/api/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "model": settings.IBM_GRANITE_MODEL_ID}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
