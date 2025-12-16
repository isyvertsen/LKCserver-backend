"""API endpoints for dashboard statistics."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.api.deps import get_db, get_current_user
from app.models.kunder import Kunder
from app.models.ansatte import Ansatte
from app.models.produkter import Produkter as ProdukterModel
from app.models.kalkyle import Kalkyle
from app.models.meny import Meny
from app.models.ordrer import Ordrer
from app.domain.entities.user import User
from pydantic import BaseModel

router = APIRouter()


class DashboardStats(BaseModel):
    """Dashboard statistics response."""
    total_customers: int
    total_employees: int
    total_products: int
    total_orders: int
    total_menus: int
    total_recipes: int


@router.get("/", response_model=DashboardStats)
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Hent dashboard-statistikk effektivt.
    Returnerer kun antall for hver entitet uten å hente alle data.
    """

    # Tell alle entiteter i parallell med COUNT queries
    customers_result = await db.execute(
        select(func.count()).select_from(Kunder)
    )
    total_customers = customers_result.scalar() or 0

    employees_result = await db.execute(
        select(func.count()).select_from(Ansatte)
    )
    total_employees = employees_result.scalar() or 0

    products_result = await db.execute(
        select(func.count()).select_from(ProdukterModel)
    )
    total_products = products_result.scalar() or 0

    orders_result = await db.execute(
        select(func.count()).select_from(Ordrer)
    )
    total_orders = orders_result.scalar() or 0

    menus_result = await db.execute(
        select(func.count()).select_from(Meny)
    )
    total_menus = menus_result.scalar() or 0

    recipes_result = await db.execute(
        select(func.count()).select_from(Kalkyle)
    )
    total_recipes = recipes_result.scalar() or 0

    return DashboardStats(
        total_customers=total_customers,
        total_employees=total_employees,
        total_products=total_products,
        total_orders=total_orders,
        total_menus=total_menus,
        total_recipes=total_recipes
    )
