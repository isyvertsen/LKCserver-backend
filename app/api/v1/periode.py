"""API endpoints for Periode management."""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.api.deps import get_db
from app.models import Periode, PeriodeMeny, Meny
from app.schemas.periode import (
    Periode as PeriodeSchema,
    PeriodeCreate,
    PeriodeUpdate,
    PeriodeWithMenus
)

router = APIRouter()


@router.get("/", response_model=List[PeriodeSchema])
async def get_perioder(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all periods with optional date filtering."""
    query = select(Periode)
    
    if from_date:
        query = query.where(Periode.tildato >= from_date)
    if to_date:
        query = query.where(Periode.fradato <= to_date)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/active", response_model=List[PeriodeWithMenus])
async def get_active_perioder(
    date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get active periods for a specific date (default: today)."""
    if not date:
        date = datetime.now()
    
    query = select(Periode).options(
        selectinload(Periode.periode_menyer).selectinload(PeriodeMeny.meny)
    ).where(
        and_(
            Periode.fradato <= date,
            Periode.tildato >= date
        )
    )
    
    result = await db.execute(query)
    perioder = result.scalars().all()
    
    # Transform to include menus directly
    response = []
    for periode in perioder:
        periode_dict = {
            "menyperiodeid": periode.menyperiodeid,
            "ukenr": periode.ukenr,
            "fradato": periode.fradato,
            "tildato": periode.tildato,
            "menus": [pm.meny for pm in periode.periode_menyer]
        }
        response.append(periode_dict)
    
    return response


@router.get("/{periode_id}", response_model=PeriodeWithMenus)
async def get_periode(
    periode_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific period by ID."""
    query = select(Periode).options(
        selectinload(Periode.periode_menyer).selectinload(PeriodeMeny.meny)
    ).where(Periode.menyperiodeid == periode_id)
    
    result = await db.execute(query)
    periode = result.scalar_one_or_none()
    
    if not periode:
        raise HTTPException(status_code=404, detail="Period not found")
    
    # Transform to include menus directly
    periode_dict = {
        "menyperiodeid": periode.menyperiodeid,
        "ukenr": periode.ukenr,
        "fradato": periode.fradato,
        "tildato": periode.tildato,
        "menus": [pm.meny for pm in periode.periode_menyer]
    }
    
    return periode_dict


@router.post("/", response_model=PeriodeSchema)
async def create_periode(
    periode_in: PeriodeCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new period."""
    periode = Periode(**periode_in.dict())
    db.add(periode)
    await db.commit()
    await db.refresh(periode)
    return periode


@router.put("/{periode_id}", response_model=PeriodeSchema)
async def update_periode(
    periode_id: int,
    periode_in: PeriodeUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing period."""
    query = select(Periode).where(Periode.menyperiodeid == periode_id)
    result = await db.execute(query)
    periode = result.scalar_one_or_none()
    
    if not periode:
        raise HTTPException(status_code=404, detail="Period not found")
    
    update_data = periode_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(periode, field, value)
    
    await db.commit()
    await db.refresh(periode)
    return periode


@router.delete("/{periode_id}")
async def delete_periode(
    periode_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a period."""
    query = select(Periode).where(Periode.menyperiodeid == periode_id)
    result = await db.execute(query)
    periode = result.scalar_one_or_none()
    
    if not periode:
        raise HTTPException(status_code=404, detail="Period not found")
    
    await db.delete(periode)
    await db.commit()
    return {"message": "Period deleted successfully"}