from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.crud import product

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=ProductResponse)
async def create_product(product_data: ProductCreate, session: Session = Depends(get_db)):
    return await product.create_product(session, product_data)

@router.get("", response_model=list[ProductResponse])
async def list_products(skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    return await product.get_products(session, skip, limit)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, session: Session = Depends(get_db)):
    result = await product.get_product(session, product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return result

@router.get("/low-stock/alerts", response_model=list[ProductResponse])
async def get_low_stock_alerts(session: Session = Depends(get_db)):
    return await product.get_low_stock_products(session)

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product_data: ProductUpdate, session: Session = Depends(get_db)):
    result = await product.update_product(session, product_id, product_data)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return result

@router.patch("/{product_id}/stock", response_model=ProductResponse)
async def update_stock(product_id: str, quantity: int, session: Session = Depends(get_db)):
    result = await product.update_stock(session, product_id, quantity)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return result
