from fastapi import FastAPI
from app.routers import product, inventory, sales, stats


app = FastAPI(
    title="E-Commerce Admin Backend Project",
    description="Backend API's products, inventory, sales and revenue analytics."
)

# Registering routers
app.include_router(product.router, tags=["Products"])
app.include_router(inventory.router, tags=["Inventory"])
app.include_router(sales.router, tags=["Sales"])
app.include_router(stats.router, tags=["Stats & Reports"])

@app.get("/")
def home():
    return {"message": "Now Testing API is running!"}
