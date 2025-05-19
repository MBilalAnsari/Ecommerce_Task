from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_, func
from app.db.database import SessionLocal
from app.models.models import Sale, Inventory, Product
from datetime import datetime
from typing import Optional

router = APIRouter()

# Dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

# Schema for creating a sale
class SaleCreate(BaseModel):
    product_id: int
    amount: float
    date: datetime

# POST for Sale => record sale, reduce stock
@router.post("/sales")
async def create_sale(sale: SaleCreate, db: AsyncSession = Depends(get_db)):
 
    # Record a new sale and reduce inventory for the product.
    result = await db.execute(select(Inventory).where(Inventory.product_id == sale.product_id))
    inventory = result.scalars().first()

    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    if inventory.quantity <= 0:
        raise HTTPException(status_code=400, detail="Out of stock")

    inventory.quantity -= 1  # ==> One unit sold
    new_sale = Sale(**sale.dict())
    db.add(new_sale)

    await db.commit()
    await db.refresh(new_sale)

    return new_sale

# => GET Sales => get all sales
@router.get("/sales")
async def get_sales(
    product_id: Optional[int] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    # Fetch sales history with optional filters by product and date range.
    query = select(Sale).options(selectinload(Sale.product))
    filters = []

    if product_id:
        filters.append(Sale.product_id == product_id)
    if start_date and end_date:
        filters.append(Sale.date.between(start_date, end_date))

    if filters:
        query = query.where(and_(*filters))

    result = await db.execute(query)
    sales = result.scalars().all()

    return [
        {
            "id": s.id,
            "product_id": s.product_id,
            "product_name": s.product.name if s.product else None,
            "amount": s.amount,
            "date": s.date
        }
        for s in sales
    ]

# GET for revenue => daily, monthly, yearly revenue
@router.get("/revenue")
async def get_revenue(
    period: str = Query("daily"),
    db: AsyncSession = Depends(get_db)
):
    # Generate total revenue grouped by day, month, or year.
    format_map = {
        "daily": "%Y-%m-%d",
        "monthly": "%Y-%m",
        "yearly": "%Y"
    }

    if period not in format_map:
        raise HTTPException(status_code=400, detail="Invalid period")

    fmt = format_map[period]

    result = await db.execute(
        select(
            func.date_format(Sale.date, fmt).label("period"),
            func.sum(Sale.amount).label("total_revenue")
        ).group_by("period").order_by("period")
    )

    return [{"period": r[0], "revenue": r[1]} for r in result]
