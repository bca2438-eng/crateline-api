from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.product import Product
from app.models.stock import StockLog
from app.auth.auth_bearer import get_current_user

router = APIRouter(prefix="/stock", tags=["Stock"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/update")
def update_stock(pid: int, amount: int, type: str = "IN",
                 db: Session = Depends(get_db),
                 user=Depends(get_current_user)):
    product = db.query(Product).filter(Product.pid == pid).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if type == "IN":
        product.quantity += amount
    elif type == "OUT":
        if product.quantity < amount:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        product.quantity -= amount
    else:
        raise HTTPException(status_code=400, detail="Type must be IN or OUT")

    log = StockLog(pid=pid, change_amount=amount, type=type)
    db.add(log)
    db.commit()
    db.refresh(product)
    return {"message": "Stock updated", "new_quantity": product.quantity}

@router.get("/logs/{pid}")
def get_stock_logs(pid: int, db: Session = Depends(get_db),
                   user=Depends(get_current_user)):
    logs = db.query(StockLog).filter(StockLog.pid == pid).all()
    return logs