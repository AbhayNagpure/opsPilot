from fastapi import FastAPI
from sqlalchemy import text
from app.api.organizations import router as organizations_router
from app.core.config import settings
from app.core.database import engine
from app.api.users import router as users_router
from app.api.memberships import router as memberships_router
from app.api.auth import router as auth_router

app = FastAPI(
    title=settings.app_name,
    description="AI-powered business workflow automation platform",
    version="0.1.0",
)
app.include_router(organizations_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(memberships_router)

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