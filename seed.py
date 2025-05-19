import asyncio
from datetime import datetime, timedelta
from app.db.database import engine, SessionLocal
from app.models.models import Product, Inventory, Sale
from sqlalchemy.ext.asyncio import AsyncSession
import random

products_data = [
    {"name": "Laptop", "description": "Core i7 Laptop", "price": 120000, "category": "Electronics"},
    {"name": "Headphones", "description": "Noise Cancelling", "price": 8000, "category": "Accessories"},
    {"name": "Coffee Mug", "description": "Thermal Mug", "price": 1200, "category": "Kitchen"},
    {"name": "Keyboard", "description": "Mechanical RGB", "price": 5000, "category": "Electronics"},
    {"name": "Backpack", "description": "Waterproof", "price": 3500, "category": "Travel"}
]

async def seed_data():
    async with SessionLocal() as session:  
        # Add Products
        products = [Product(**data) for data in products_data]
        session.add_all(products)
        await session.commit()
        await session.refresh(products[0])  

        #  Add Inventory
        for product in products:
            inventory = Inventory(product_id=product.id, quantity=random.randint(5, 20))
            session.add(inventory)
        
        await session.commit()

        #  Add Random Sales
        for _ in range(10):
            product = random.choice(products)
            days_ago = random.randint(0, 30)
            sale_date = datetime.now() - timedelta(days=days_ago)
            amount = product.price
            sale = Sale(product_id=product.id, amount=amount, date=sale_date)
            session.add(sale)

        await session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":

    asyncio.run(seed_data())

