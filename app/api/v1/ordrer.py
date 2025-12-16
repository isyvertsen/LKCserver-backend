"""Order API endpoints."""
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import select, func, desc, asc
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.deps import get_db, get_current_user
from app.domain.entities.user import User
from app.models.ordrer import Ordrer as OrdrerModel
from app.models.ordredetaljer import Ordredetaljer as OrdredetaljerModel
from app.models.kunder import Kunder as KunderModel
from app.schemas.ordrer import Ordrer, OrdrerCreate, OrdrerUpdate
from app.schemas.ordredetaljer import Ordredetaljer, OrdredetaljerCreate
from app.schemas.pagination import PaginatedResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[Ordrer])
async def get_ordrer(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    kunde_id: Optional[int] = Query(None, description="Filter by customer ID"),
    fra_dato: Optional[date] = Query(None, description="From date"),
    til_dato: Optional[date] = Query(None, description="To date"),
    kundegruppe_ids: Optional[List[int]] = Query(None, description="Filter by customer group IDs"),
    sort_by: Optional[str] = Query("leveringsdato", description="Sort field (leveringsdato or ordredato)"),
    sort_order: Optional[str] = Query("asc", description="Sort order (asc or desc)"),
) -> PaginatedResponse[Ordrer]:
    """Get all orders."""
    # Base query for counting
    count_query = select(func.count()).select_from(OrdrerModel)
    
    # Data query with customer join
    query = select(OrdrerModel).options(joinedload(OrdrerModel.kunde))
    
    # Apply filters to both queries
    if kunde_id:
        count_query = count_query.where(OrdrerModel.kundeid == kunde_id)
        query = query.where(OrdrerModel.kundeid == kunde_id)
    
    if fra_dato:
        count_query = count_query.where(OrdrerModel.ordredato >= fra_dato)
        query = query.where(OrdrerModel.ordredato >= fra_dato)
    if til_dato:
        count_query = count_query.where(OrdrerModel.ordredato <= til_dato)
        query = query.where(OrdrerModel.ordredato <= til_dato)
    
    # Filter by customer groups if specified
    if kundegruppe_ids:
        # Need to join with customers to filter by kundegruppe
        from app.models.kunder import Kunder as KunderModel
        count_query = count_query.join(KunderModel, OrdrerModel.kundeid == KunderModel.kundeid)
        count_query = count_query.where(KunderModel.kundegruppe.in_(kundegruppe_ids))
        
        query = query.join(KunderModel, OrdrerModel.kundeid == KunderModel.kundeid)
        query = query.where(KunderModel.kundegruppe.in_(kundegruppe_ids))
    
    # Get total count
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Apply sorting
    if sort_by == "leveringsdato":
        sort_column = OrdrerModel.leveringsdato
    elif sort_by == "ordredato":
        sort_column = OrdrerModel.ordredato
    else:
        sort_column = OrdrerModel.leveringsdato  # Default
    
    if sort_order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))
    
    # Get paginated data
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()
    
    # Update kundenavn and kundegruppenavn from the joined customer data
    for item in items:
        if hasattr(item, 'kunde') and item.kunde:
            if not item.kundenavn:
                item.kundenavn = item.kunde.kundenavn
            # Add customer group name
            if hasattr(item.kunde, 'gruppe') and item.kunde.gruppe:
                item.kundegruppenavn = item.kunde.gruppe.gruppe
    
    # Calculate pagination info
    page = (skip // limit) + 1
    total_pages = (total + limit - 1) // limit if total > 0 else 0
    
    return PaginatedResponse[Ordrer](
        items=items,
        total=total,
        page=page,
        page_size=limit,
        total_pages=total_pages
    )


@router.get("/{ordre_id}", response_model=Ordrer)
async def get_ordre(
    ordre_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Ordrer:
    """Get an order by ID."""
    result = await db.execute(
        select(OrdrerModel)
        .options(joinedload(OrdrerModel.kunde))
        .where(OrdrerModel.ordreid == ordre_id)
    )
    ordre = result.scalar_one_or_none()
    
    if not ordre:
        raise HTTPException(status_code=404, detail="Ordre ikke funnet")
    
    # Update kundenavn and kundegruppenavn from the joined customer data
    if hasattr(ordre, 'kunde') and ordre.kunde:
        if not ordre.kundenavn:
            ordre.kundenavn = ordre.kunde.kundenavn
        # Add customer group name
        if hasattr(ordre.kunde, 'gruppe') and ordre.kunde.gruppe:
            ordre.kundegruppenavn = ordre.kunde.gruppe.gruppe
    
    return ordre


@router.get("/{ordre_id}/detaljer", response_model=List[Ordredetaljer])
async def get_ordre_detaljer(
    ordre_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[Ordredetaljer]:
    """Get order details."""
    result = await db.execute(
        select(OrdredetaljerModel).where(OrdredetaljerModel.ordreid == ordre_id)
    )
    return result.scalars().all()


@router.post("/", response_model=Ordrer)
async def create_ordre(
    ordre_data: OrdrerCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Ordrer:
    """Create a new order."""
    ordre = OrdrerModel(**ordre_data.model_dump())
    db.add(ordre)
    await db.commit()
    await db.refresh(ordre)
    return ordre


@router.post("/{ordre_id}/detaljer", response_model=Ordredetaljer)
async def add_ordre_detalj(
    ordre_id: int,
    detalj_data: OrdredetaljerCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Ordredetaljer:
    """Add detail to an order."""
    # Check if order exists
    result = await db.execute(
        select(OrdrerModel).where(OrdrerModel.ordreid == ordre_id)
    )
    ordre = result.scalar_one_or_none()
    
    if not ordre:
        raise HTTPException(status_code=404, detail="Ordre ikke funnet")
    
    # Get next unik value
    max_unik_result = await db.execute(
        select(func.max(OrdredetaljerModel.unik)).where(
            OrdredetaljerModel.ordreid == ordre_id
        )
    )
    max_unik = max_unik_result.scalar() or 0
    
    detalj = OrdredetaljerModel(
        ordreid=ordre_id,
        unik=max_unik + 1,
        **detalj_data.model_dump()
    )
    db.add(detalj)
    await db.commit()
    await db.refresh(detalj)
    return detalj


@router.put("/{ordre_id}", response_model=Ordrer)
async def update_ordre(
    ordre_id: int,
    ordre_data: OrdrerUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Ordrer:
    """Update an order."""
    result = await db.execute(
        select(OrdrerModel).where(OrdrerModel.ordreid == ordre_id)
    )
    ordre = result.scalar_one_or_none()
    
    if not ordre:
        raise HTTPException(status_code=404, detail="Ordre ikke funnet")
    
    update_data = ordre_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ordre, field, value)
    
    await db.commit()
    await db.refresh(ordre)
    return ordre


@router.delete("/{ordre_id}")
async def cancel_ordre(
    ordre_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Cancel an order."""
    result = await db.execute(
        select(OrdrerModel).where(OrdrerModel.ordreid == ordre_id)
    )
    ordre = result.scalar_one_or_none()
    
    if not ordre:
        raise HTTPException(status_code=404, detail="Ordre ikke funnet")
    
    ordre.kansellertdato = datetime.now()
    ordre.ordrestatusid = 5  # Cancelled status
    await db.commit()
    
    return {"message": "Ordre kansellert"}