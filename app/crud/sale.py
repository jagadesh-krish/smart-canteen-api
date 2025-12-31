from sqlmodel import Session, select, func
from sqlalchemy import and_
from datetime import datetime
from app.models.sale import Sale, SaleItem
from app.models.product import Product
from app.models.customer import Customer
from app.schemas.sale import SaleCreate
from app.crud.product import update_stock

def generate_invoice_number() -> str:
    now = datetime.utcnow()
    timestamp = now.strftime("%Y%m%d%H%M%S%f")[:-2]
    return f"INV-{timestamp}"

async def create_sale(session: Session, sale: SaleCreate) -> Sale:
    customer = await session.get(Customer, sale.customer_id)
    if not customer:
        raise ValueError("Customer not found")

    total_amount = 0
    sale_items = []

    for item in sale.items:
        product = await session.get(Product, item.product_id)
        if not product:
            raise ValueError(f"Product {item.product_id} not found")

        if product.stock_quantity < item.quantity:
            raise ValueError(f"Insufficient stock for {product.name}")

        line_total = item.quantity * item.unit_price
        total_amount += line_total
        sale_items.append((item, line_total, product))

    grand_total = total_amount + sale.tax_amount - sale.discount_amount

    db_sale = Sale(
        invoice_number=generate_invoice_number(),
        customer_id=sale.customer_id,
        total_amount=total_amount,
        tax_amount=sale.tax_amount,
        discount_amount=sale.discount_amount,
        grand_total=grand_total,
        notes=sale.notes,
    )
    session.add(db_sale)
    await session.flush()

    for item, line_total, product in sale_items:
        db_item = SaleItem(
            sale_id=db_sale.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            line_total=line_total,
        )
        session.add(db_item)
        product.stock_quantity -= item.quantity
        session.add(product)

    await session.commit()
    await session.refresh(db_sale)
    return db_sale

async def get_sale(session: Session, sale_id: str):
    return await session.get(Sale, sale_id)

async def get_sales(session: Session, skip: int = 0, limit: int = 100):
    result = await session.execute(select(Sale).offset(skip).limit(limit))
    return result.scalars().all()

async def get_sale_by_invoice(session: Session, invoice_number: str):
    result = await session.execute(select(Sale).where(Sale.invoice_number == invoice_number))
    return result.scalar_one_or_none()

async def get_sales_by_customer(session: Session, customer_id: str):
    result = await session.execute(select(Sale).where(Sale.customer_id == customer_id))
    return result.scalars().all()

async def update_sale_status(session: Session, sale_id: str, status: str):
    db_sale = await session.get(Sale, sale_id)
    if db_sale:
        db_sale.status = status
        session.add(db_sale)
        await session.commit()
        await session.refresh(db_sale)
    return db_sale

async def get_monthly_report(session: Session, year: int, month: int):
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    result = await session.execute(
        select(
            func.count(Sale.id).label("total_sales"),
            func.sum(Sale.grand_total).label("total_revenue"),
            func.avg(Sale.grand_total).label("average_order_value"),
        ).where(and_(Sale.sale_date >= start_date, Sale.sale_date < end_date))
    )
    row = result.one()
    return {
        "total_sales": row.total_sales or 0,
        "total_revenue": float(row.total_revenue or 0),
        "average_order_value": float(row.average_order_value or 0),
    }

async def get_top_products(session: Session, limit: int = 10):
    result = await session.execute(
        select(
            Product.id,
            Product.name,
            func.sum(SaleItem.quantity).label("total_quantity"),
        )
        .join(SaleItem, SaleItem.product_id == Product.id)
        .group_by(Product.id, Product.name)
        .order_by(func.sum(SaleItem.quantity).desc())
        .limit(limit)
    )
    return [
        {
            "product_id": row.id,
            "product_name": row.name,
            "total_quantity": row.total_quantity,
        }
        for row in result
    ]
