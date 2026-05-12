from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.category import Category
from app.models.product import Product
from app.schemas.category import CategoryCreate
from app.auth.auth_bearer import get_current_user, require_admin

router = APIRouter(prefix="/categories", tags=["Categories"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, db: Session = Depends(get_db),
                    user=Depends(require_admin)):
    existing = db.query(Category).filter(Category.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Category '{data.name}' already exists")
    category = Category(name=data.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.delete("/{cid}")
def delete_category(cid: int, db: Session = Depends(get_db),
                    user=Depends(require_admin)):
    category = db.query(Category).filter(Category.cid == cid).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category with id {cid} not found")
    products = db.query(Product).filter(Product.category_id == cid).first()
    if products:
        raise HTTPException(status_code=400, detail="Cannot delete category — products are assigned to it.")
    db.delete(category)
    db.commit()
    return {"message": f"Category '{category.name}' deleted successfully"}