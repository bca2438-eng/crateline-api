from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import SessionLocal
from app.models.audit_log import AuditLog
from app.auth.auth_bearer import get_current_user, require_admin

router = APIRouter(prefix="/audit", tags=["Audit Logs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_audit_logs(
    db: Session = Depends(get_db),
    user=Depends(require_admin),
    resource: Optional[str] = Query(None),
    action: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    query = db.query(AuditLog).order_by(AuditLog.created_at.desc())

    if resource:
        query = query.filter(AuditLog.resource == resource)
    if action:
        query = query.filter(AuditLog.action == action)

    total = query.count()
    logs = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "pages": max((total + limit - 1) // limit, 1),
        "data": logs
    }