from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class StockLog(Base):
    __tablename__ = "stock_logs"

    log_id = Column(Integer, primary_key=True, index=True)
    pid = Column(Integer, ForeignKey("products.pid"), nullable=False)
    change_amount = Column(Integer, nullable=False)
    type = Column(String(10), nullable=False)  # "IN" or "OUT"
    created_at = Column(DateTime, default=datetime.utcnow)