from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import SessionLocal
from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate
from app.auth.auth_bearer import get_current_user, require_admin
from app.utils.audit_helper import log_action

router = APIRouter(prefix="/products", tags=["Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_products(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    search: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    low_stock: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    include_inactive: bool = Query(False),
):
    query = db.query(Product)
    if not include_inactive:
        query = query.filter(Product.is_active == True)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if low_stock:
        query = query.filter(Product.quantity < Product.reorder_level)

    total = query.count()
    products = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "pages": max((total + limit - 1) // limit, 1),
        "data": products
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, db: Session = Depends(get_db),
                   user=Depends(require_admin)):
    category = db.query(Category).filter(Category.cid == data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category with id {data.category_id} not found")
    existing = db.query(Product).filter(Product.name == data.name, Product.is_active == True).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Product '{data.name}' already exists")
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    log_action(db, user, "CREATE", "product", product.pid, f"Created product: {product.name}")
    return product

@router.put("/{pid}")
def update_product(pid: int, data: ProductCreate, db: Session = Depends(get_db),
                   user=Depends(require_admin)):
    product = db.query(Product).filter(Product.pid == pid, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {pid} not found")
    category = db.query(Category).filter(Category.cid == data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category with id {data.category_id} not found")
    old_name = product.name
    product.name = data.name
    product.price = data.price
    product.quantity = data.quantity
    product.category_id = data.category_id
    product.reorder_level = data.reorder_level
    db.commit()
    db.refresh(product)
    log_action(db, user, "UPDATE", "product", pid, f"Updated product: {old_name}")
    return product

@router.delete("/{pid}")
def delete_product(pid: int, db: Session = Depends(get_db),
                   user=Depends(require_admin)):
    product = db.query(Product).filter(Product.pid == pid, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {pid} not found")
    product.is_active = False
    db.commit()
    log_action(db, user, "DELETE", "product", pid, f"Soft deleted product: {product.name}")
    return {"message": f"Product '{product.name}' deactivated successfully"}

@router.put("/{pid}/restore")
def restore_product(pid: int, db: Session = Depends(get_db),
                    user=Depends(require_admin)):
    product = db.query(Product).filter(Product.pid == pid, Product.is_active == False).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product not found or already active")
    product.is_active = True
    db.commit()
    log_action(db, user, "RESTORE", "product", pid, f"Restored product: {product.name}")
    return {"message": f"Product '{product.name}' restored successfully"}