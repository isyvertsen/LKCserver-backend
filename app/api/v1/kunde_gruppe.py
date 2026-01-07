"""Customer group API endpoints."""
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_db, get_current_user
from app.domain.entities.user import User
from app.models.kunde_gruppe import Kundegruppe as KundegruppeModel
from app.schemas.kunde_gruppe import Kundegruppe, KundegruppeCreate, KundegruppeUpdate

router = APIRouter()


@router.get("/", response_model=List[Kundegruppe])
async def get_kundegrupper(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[Kundegruppe]:
    """Get all customer groups."""
    result = await db.execute(select(KundegruppeModel).order_by(KundegruppeModel.gruppe))
    return result.scalars().all()


@router.get("/{gruppe_id}", response_model=Kundegruppe)
async def get_kundegruppe(
    gruppe_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Kundegruppe:
    """Get a customer group by ID."""
    result = await db.execute(
        select(KundegruppeModel).where(KundegruppeModel.gruppeid == gruppe_id)
    )
    gruppe = result.scalar_one_or_none()
    if not gruppe:
        raise HTTPException(status_code=404, detail="Kundegruppe ikke funnet")
    return gruppe


@router.post("/", response_model=Kundegruppe)
async def create_kundegruppe(
    data: KundegruppeCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Kundegruppe:
    """Create a new customer group."""
    gruppe = KundegruppeModel(
        gruppe=data.gruppe,
        webshop=data.webshop,
        autofaktura=data.autofaktura,
    )
    db.add(gruppe)
    await db.commit()
    await db.refresh(gruppe)
    return gruppe


@router.put("/{gruppe_id}", response_model=Kundegruppe)
async def update_kundegruppe(
    gruppe_id: int,
    data: KundegruppeUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Kundegruppe:
    """Update a customer group."""
    result = await db.execute(
        select(KundegruppeModel).where(KundegruppeModel.gruppeid == gruppe_id)
    )
    gruppe = result.scalar_one_or_none()
    if not gruppe:
        raise HTTPException(status_code=404, detail="Kundegruppe ikke funnet")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(gruppe, field, value)

    await db.commit()
    await db.refresh(gruppe)
    return gruppe


@router.delete("/{gruppe_id}")
async def delete_kundegruppe(
    gruppe_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Delete a customer group."""
    result = await db.execute(
        select(KundegruppeModel).where(KundegruppeModel.gruppeid == gruppe_id)
    )
    gruppe = result.scalar_one_or_none()
    if not gruppe:
        raise HTTPException(status_code=404, detail="Kundegruppe ikke funnet")

    await db.delete(gruppe)
    await db.commit()
    return {"message": "Kundegruppe slettet"}