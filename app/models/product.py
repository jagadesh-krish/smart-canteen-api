from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Product(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(index=True)
    sku: str = Field(unique=True, index=True)
    description: Optional[str] = None
    category: Optional[str] = None
    price: float = Field(gt=0)
    stock_quantity: int = Field(ge=0)
    low_stock_threshold: int = Field(default=10, ge=0)
    unit: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
