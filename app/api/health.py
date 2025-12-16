"""Health check endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.infrastructure.database.session import get_db

router = APIRouter()


@router.get("/")
async def health():
    """Basic health check."""
    return {"status": "healthy", "service": "catering-api"}


@router.get("/ready")
async def readiness(db: AsyncSession = Depends(get_db)):
    """Readiness check including database connectivity."""
    try:
        # Test database connection
        await db.execute(text("SELECT 1"))
        return {
            "status": "ready",
            "checks": {
                "database": "connected",
            }
        }
    except Exception as e:
        return {
            "status": "not ready",
            "checks": {
                "database": f"error: {str(e)}",
            }
        }