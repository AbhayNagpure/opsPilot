from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine


app = FastAPI(
    title=settings.app_name,
    description="AI-powered business workflow automation platform",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "message": settings.app_name,
        "environment": settings.app_env,
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.app_env,
    }


@app.get("/health/db")
async def database_health_check():
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "database": "connected",
        "result": result.scalar(),
    }