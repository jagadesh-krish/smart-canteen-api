from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.crud import customer

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("", response_model=CustomerResponse)
async def create_customer(customer_data: CustomerCreate, session: Session = Depends(get_db)):
    return await customer.create_customer(session, customer_data)

@router.get("", response_model=list[CustomerResponse])
async def list_customers(skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    return await customer.get_customers(session, skip, limit)

@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: str, session: Session = Depends(get_db)):
    result = await customer.get_customer(session, customer_id)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return result

@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(customer_id: str, customer_data: CustomerUpdate, session: Session = Depends(get_db)):
    result = await customer.update_customer(session, customer_id, customer_data)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return result

