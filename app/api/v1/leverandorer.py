"""Supplier API endpoints."""
from typing import List, Optional
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.deps import get_db, get_current_user
from app.domain.entities.user import User
from app.models.leverandorer import Leverandorer as LeverandorerModel
from app.schemas.leverandorer import Leverandorer, LeverandorerCreate, LeverandorerUpdate

router = APIRouter()


@router.get("/", response_model=List[Leverandorer])
async def get_leverandorer(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    aktiv: Optional[bool] = Query(True, description="Filter by active status"),
) -> List[Leverandorer]:
    """Get all suppliers."""
    query = select(LeverandorerModel)
    
    # Filter by utgatt status (inverted - utgatt=False means active)
    if aktiv is not None:
        if aktiv:
            query = query.where(
                or_(LeverandorerModel.utgatt == False, LeverandorerModel.utgatt == None)
            )
        else:
            query = query.where(LeverandorerModel.utgatt == True)
    
    query = query.order_by(LeverandorerModel.leverandornavn).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{leverandor_id}", response_model=Leverandorer)
async def get_leverandor(
    leverandor_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Leverandorer:
    """Get a supplier by ID."""
    result = await db.execute(
        select(LeverandorerModel).where(LeverandorerModel.leverandorid == leverandor_id)
    )
    leverandor = result.scalar_one_or_none()
    
    if not leverandor:
        raise HTTPException(status_code=404, detail="Leverandør ikke funnet")
    
    return leverandor


@router.post("/", response_model=Leverandorer)
async def create_leverandor(
    leverandor_data: LeverandorerCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Leverandorer:
    """Create a new supplier."""
    leverandor = LeverandorerModel(**leverandor_data.model_dump())
    db.add(leverandor)
    await db.commit()
    await db.refresh(leverandor)
    return leverandor


@router.put("/{leverandor_id}", response_model=Leverandorer)
async def update_leverandor(
    leverandor_id: int,
    leverandor_data: LeverandorerUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Leverandorer:
    """Update a supplier."""
    result = await db.execute(
        select(LeverandorerModel).where(LeverandorerModel.leverandorid == leverandor_id)
    )
    leverandor = result.scalar_one_or_none()
    
    if not leverandor:
        raise HTTPException(status_code=404, detail="Leverandør ikke funnet")
    
    update_data = leverandor_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(leverandor, field, value)
    
    await db.commit()
    await db.refresh(leverandor)
    return leverandor


@router.delete("/{leverandor_id}")
async def delete_leverandor(
    leverandor_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Delete a supplier (soft delete by setting utgatt=True)."""
    result = await db.execute(
        select(LeverandorerModel).where(LeverandorerModel.leverandorid == leverandor_id)
    )
    leverandor = result.scalar_one_or_none()
    
    if not leverandor:
        raise HTTPException(status_code=404, detail="Leverandør ikke funnet")
    
    leverandor.utgatt = True
    await db.commit()
    
    return {"message": "Leverandør deaktivert"}