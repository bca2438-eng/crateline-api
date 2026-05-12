from pydantic import BaseModel
from datetime import datetime

class StockLogOut(BaseModel):
    log_id: int
    pid: int
    change_amount: int
    type: str
    created_at: datetime

    class Config:
        from_attributes = True