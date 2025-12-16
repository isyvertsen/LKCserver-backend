"""Customer group API endpoints."""
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.api.deps import get_db, get_current_user
from app.domain.entities.user import User
from app.models.kunde_gruppe import Kundegruppe as KundegruppeModel
from app.schemas.kunde_gruppe import Kundegruppe

router = APIRouter()


@router.get("/", response_model=List[Kundegruppe])
async def get_kundegrupper(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[Kundegruppe]:
    """Get all customer groups."""
    result = await db.execute(select(KundegruppeModel).order_by(KundegruppeModel.gruppe))
    return result.scalars().all()