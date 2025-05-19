from fastapi import APIRouter, Depends, HTTPException , Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import Product
from app.db.database import SessionLocal
from pydantic import BaseModel

router = APIRouter()

# => pydantic schema for creating a product
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str

# => Dependency to get the database session
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

# => Post /products =>  create product
@router.post("/products")
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):

    # add new product to the catalog
    new_product = Product(**product.dict())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product
 
 # => Get /products =>  get sum of the   products
@router.get("/products")
async def get_products(db: AsyncSession = Depends(get_db)):

    # Fetch for all products
    results = await db.execute(select(Product))
    products = results.scalars().all()
    return products

# => Get /products/{product_id} =>  get product by id
@router.get("/products/search")
async def search_products(name: str = Query(..., description="Partial name to search"), db: AsyncSession = Depends(get_db)):

    # Search products by name (case-insensitive).
    result = await db.execute(
        select(Product).where(Product.name.ilike(f"%{name}%"))
    )
    return result.scalars().all()