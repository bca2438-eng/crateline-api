from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.product import Product
from app.models.stock import StockLog
from app.auth.auth_bearer import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_dashboard(db: Session = Depends(get_db), user=Depends(get_current_user)):
    total_products = db.query(Product).count()
    low_stock = db.query(Product).filter(Product.quantity < Product.reorder_level).count()
    total_stock_value = db.query(Product).all()
    stock_value = sum(float(p.price) * p.quantity for p in total_stock_value)

    return {
        "total_products": total_products,
        "low_stock_alerts": low_stock,
        "total_stock_value": round(stock_value, 2)
    }

@router.get("/low-stock")
def get_low_stock(db: Session = Depends(get_db), user=Depends(get_current_user)):
    products = db.query(Product).filter(Product.quantity < Product.reorder_level).all()
    return products