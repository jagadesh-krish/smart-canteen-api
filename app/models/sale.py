from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class SaleItem(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    sale_id: str = Field(foreign_key="sale.id")
    product_id: str = Field(foreign_key="product.id")
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    line_total: float = Field(gt=0)

class Sale(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    invoice_number: str = Field(unique=True, index=True)
    customer_id: str = Field(foreign_key="customer.id")
    sale_date: datetime = Field(default_factory=datetime.utcnow)
    total_amount: float = Field(default=0)
    tax_amount: float = Field(default=0)
    discount_amount: float = Field(default=0)
    grand_total: float = Field(default=0)
    status: str = Field(default="completed")
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
