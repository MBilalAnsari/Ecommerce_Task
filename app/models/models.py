from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
# inside Inventory model
product = relationship("Product", back_populates="inventory")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(225))
    price = Column(Float)
    category = Column(String(100))

    # Relationships
    inventory = relationship("Inventory", back_populates="product")
    sales = relationship("Sale", back_populates="product")


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

    # Relationship to product
    product = relationship("Product", back_populates="inventory")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    amount = Column(Float)
    date = Column(DateTime)

    # Relationship to product
    product = relationship("Product", back_populates="sales")