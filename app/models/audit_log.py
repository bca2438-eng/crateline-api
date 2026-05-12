from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.uid"), nullable=True)
    user_email = Column(String(255), nullable=True)
    action = Column(String(100), nullable=False)  # CREATE, UPDATE, DELETE, RESTORE, LOGIN
    resource = Column(String(100), nullable=False)  # product, category, stock, auth
    resource_id = Column(Integer, nullable=True)
    details = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now())