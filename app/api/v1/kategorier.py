"""Category API endpoints."""
from typing import List, Optional
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.deps import get_db, get_current_user
from app.domain.entities.user import User
from app.models.kategorier import Kategorier as KategorierModel
from app.schemas.kategorier import Kategorier, KategorierCreate, KategorierUpdate

router = APIRouter()


@router.get("/", response_model=List[Kategorier])
async def get_kategorier(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None, description="Search by name or description"),
) -> List[Kategorier]:
    """Get all categories."""
    query = select(KategorierModel)

    # Search filter
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                KategorierModel.kategori.ilike(search_term),
                KategorierModel.beskrivelse.ilike(search_term),
            )
        )

    query = query.order_by(KategorierModel.kategori).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{kategori_id}", response_model=Kategorier)
async def get_kategori(
    kategori_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Kategorier:
    """Get a category by ID."""
    result = await db.execute(
        select(KategorierModel).where(KategorierModel.kategoriid == kategori_id)
    )
    kategori = result.scalar_one_or_none()
    
    if not kategori:
        raise HTTPException(status_code=404, detail="Kategori ikke funnet")
    
    return kategori


@router.post("/", response_model=Kategorier)
async def create_kategori(
    kategori_data: KategorierCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Kategorier:
    """Create a new category."""
    kategori = KategorierModel(**kategori_data.model_dump())
    db.add(kategori)
    await db.commit()
    await db.refresh(kategori)
    return kategori


@router.put("/{kategori_id}", response_model=Kategorier)
async def update_kategori(
    kategori_id: int,
    kategori_data: KategorierUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Kategorier:
    """Update a category."""
    result = await db.execute(
        select(KategorierModel).where(KategorierModel.kategoriid == kategori_id)
    )
    kategori = result.scalar_one_or_none()
    
    if not kategori:
        raise HTTPException(status_code=404, detail="Kategori ikke funnet")
    
    update_data = kategori_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(kategori, field, value)
    
    await db.commit()
    await db.refresh(kategori)
    return kategori


@router.delete("/{kategori_id}")
async def delete_kategori(
    kategori_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Delete a category."""
    result = await db.execute(
        select(KategorierModel).where(KategorierModel.kategoriid == kategori_id)
    )
    kategori = result.scalar_one_or_none()
    
    if not kategori:
        raise HTTPException(status_code=404, detail="Kategori ikke funnet")
    
    await db.delete(kategori)
    await db.commit()
    
    return {"message": "Kategori slettet"}