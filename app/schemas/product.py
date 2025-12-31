from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    sku: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: float
    stock_quantity: int
    low_stock_threshold: int = 10
    unit: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    low_stock_threshold: Optional[int] = None
    unit: Optional[str] = None

class ProductResponse(BaseModel):
    id: str
    name: str
    sku: str
    price: float
    stock_quantity: int
    low_stock_threshold: int
