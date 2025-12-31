from sqlmodel import Session, select
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate

async def create_customer(session: Session, customer: CustomerCreate) -> Customer:
    db_customer = Customer(**customer.model_dump())
    session.add(db_customer)
    await session.commit()
    await session.refresh(db_customer)
    return db_customer

async def get_customer(session: Session, customer_id: str):
    return await session.get(Customer, customer_id)

async def get_customers(session: Session, skip: int = 0, limit: int = 100):
    result = await session.execute(select(Customer).offset(skip).limit(limit))
    return result.scalars().all()

async def update_customer(session: Session, customer_id: str, customer: CustomerUpdate) -> Customer:
    db_customer = await session.get(Customer, customer_id)
    if db_customer:
        update_data = customer.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_customer, key, value)
        session.add(db_customer)
        await session.commit()
        await session.refresh(db_customer)
    return db_customer

