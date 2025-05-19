import asyncio
from app.db.database import engine, Base
from app.models.models import Product, Inventory, Sale

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized, models created.")

asyncio.run(init_models())
