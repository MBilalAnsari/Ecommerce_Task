from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import Inventory, Product
from app.db.database import SessionLocal
from sqlalchemy.orm import selectinload
from pydantic import BaseModel

router = APIRouter()

# => Pydantic Schemas
class InventoryUpdate(BaseModel):
    quantity: int

# => Dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

# => GET Inventory
@router.get("/inventory")
async def get_inventory(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Inventory).options(selectinload(Inventory.product))

    )
    inventory_list = result.scalars().all()
    inventory_data = []
    for item in inventory_list:
        inventory_data.append({
            "id": item.id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "low_stock": item.quantity < 10  # threshold
        })
    return inventory_data


# => PUT Inventory
@router.put("/inventory/{product_id}")
async def update_inventory(product_id: int, data: InventoryUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Inventory).where(Inventory.product_id == product_id))
    inventory = result.scalars().first()

    if inventory:
        inventory.quantity = data.quantity
    else:
        inventory = Inventory(product_id=product_id, quantity=data.quantity)
        db.add(inventory)

    await db.commit()
    await db.refresh(inventory)
    return inventory
