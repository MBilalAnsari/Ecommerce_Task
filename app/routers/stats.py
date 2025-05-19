from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.db.database import SessionLocal
from app.models.models import Product, Inventory, Sale

router = APIRouter()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

# ==> GET /stats/overview
@router.get("/stats/overview")
async def get_stats(db: AsyncSession = Depends(get_db)):
    # ==> Count total products
    total_products = (await db.execute(select(func.count(Product.id)))).scalar()

    # ==> Sum total stock
    total_stock = (await db.execute(select(func.sum(Inventory.quantity)))).scalar() or 0

    # ==> Count total sales
    total_sales = (await db.execute(select(func.count(Sale.id)))).scalar()

    # ==> Sum total revenue
    total_revenue = (await db.execute(select(func.sum(Sale.amount)))).scalar() or 0.0

    # ==> Top-selling product
    top_product_result = await db.execute(
        select(Sale.product_id, func.count(Sale.id).label("count"))
        .group_by(Sale.product_id)
        .order_by(func.count(Sale.id).desc())
        .limit(1)
    )
    top_product = top_product_result.first()
    top_product_name = None

    if top_product:
        product_result = await db.execute(
            select(Product.name).where(Product.id == top_product[0])
        )
        top_product_name = product_result.scalar()

    return {
        "total_products": total_products,
        "total_stock": total_stock,
        "total_sales": total_sales,
        "total_revenue": total_revenue,
        "top_selling_product": top_product_name or "N/A"
    }
