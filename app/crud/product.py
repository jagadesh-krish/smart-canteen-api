from sqlmodel import Session, select
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

async def create_product(session: Session, product: ProductCreate) -> Product:
    db_product = Product(**product.model_dump())
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return db_product

async def get_product(session: Session, product_id: str):
    return await session.get(Product, product_id)

async def get_products(session: Session, skip: int = 0, limit: int = 100):
    result = await session.execute(select(Product).offset(skip).limit(limit))
    return result.scalars().all()

async def get_low_stock_products(session: Session):
    result = await session.execute(
        select(Product).where(Product.stock_quantity <= Product.low_stock_threshold)
    )
    return result.scalars().all()

async def update_product(session: Session, product_id: str, product: ProductUpdate) -> Product:
    db_product = await session.get(Product, product_id)
    if db_product:
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        session.add(db_product)
        await session.commit()
        await session.refresh(db_product)
    return db_product

async def update_stock(session: Session, product_id: str, quantity: int):
    db_product = await session.get(Product, product_id)
    if db_product:
        db_product.stock_quantity = max(0, db_product.stock_quantity + quantity)
        session.add(db_product)
        await session.commit()
        await session.refresh(db_product)
    return db_product