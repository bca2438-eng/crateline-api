from app.models.audit_log import AuditLog
from sqlalchemy.orm import Session

def log_action(
    db: Session,
    user: dict,
    action: str,
    resource: str,
    resource_id: int = None,
    details: str = None
):
    try:
        audit = AuditLog(
            user_id=user.get("uid"),
            user_email=user.get("sub"),
            action=action,
            resource=resource,
            resource_id=resource_id,
            details=details
        )
        db.add(audit)
        db.commit()
    except Exception:
        pass  # Never let audit logging break the main operation