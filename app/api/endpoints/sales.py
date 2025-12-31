from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_db
from app.schemas.sale import SaleCreate, SaleResponse
from app.crud import sale

router = APIRouter(prefix="/sales", tags=["sales"])

@router.post("", response_model=SaleResponse)
async def create_sale(sale_data: SaleCreate, session: Session = Depends(get_db)):
    try:
        return await sale.create_sale(session, sale_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=list[SaleResponse])
async def list_sales(skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    return await sale.get_sales(session, skip, limit)

@router.get("/{sale_id}", response_model=SaleResponse)
async def get_sale(sale_id: str, session: Session = Depends(get_db)):
    result = await sale.get_sale(session, sale_id)
    if not result:
        raise HTTPException(status_code=404, detail="Sale not found")
    return result

@router.get("/invoice/{invoice_number}", response_model=SaleResponse)
async def get_sale_by_invoice(invoice_number: str, session: Session = Depends(get_db)):
    result = await sale.get_sale_by_invoice(session, invoice_number)
    if not result:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return result

@router.get("/customer/{customer_id}", response_model=list[SaleResponse])
async def get_customer_sales(customer_id: str, session: Session = Depends(get_db)):
    return await sale.get_sales_by_customer(session, customer_id)

@router.put("/{sale_id}", response_model=SaleResponse)
async def update_sale_status(sale_id: str, status: str, session: Session = Depends(get_db)):
    result = await sale.update_sale_status(session, sale_id, status)
    if not result:
        raise HTTPException(status_code=404, detail="Sale not found")
    return result

@router.get("/reports/monthly/{year}/{month}")
async def get_monthly_report(year: int, month: int, session: Session = Depends(get_db)):
    return await sale.get_monthly_report(session, year, month)

@router.get("/reports/top-products")
async def get_top_products(limit: int = 10, session: Session = Depends(get_db)):
    return await sale.get_top_products(session, limit)
