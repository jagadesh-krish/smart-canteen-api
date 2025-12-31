from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SaleItemCreate(BaseModel):
    product_id: str
    quantity: int
    unit_price: float

class SaleCreate(BaseModel):
    customer_id: str
    items: List[SaleItemCreate]
    tax_amount: float = 0
    discount_amount: float = 0
    notes: Optional[str] = None

class SaleResponse(BaseModel):
    id: str
    invoice_number: str
    customer_id: str
    total_amount: float
    tax_amount: float
    discount_amount: float
    grand_total: float
    status: str
    sale_date: datetime

class MonthlyReport(BaseModel):
    total_sales: int
    total_revenue: float
    average_order_value: float

class TopProduct(BaseModel):
    product_id: str
    product_name: str
    total_quantity: int
