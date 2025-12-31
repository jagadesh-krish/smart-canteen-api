from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Customer(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    company_name: str = Field(index=True)
    contact_person: str
    email: str = Field(unique=True, index=True)
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
