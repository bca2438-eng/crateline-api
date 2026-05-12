from pydantic import BaseModel, validator, Field
from typing import Optional

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    category_id: int = Field(..., gt=0)
    reorder_level: int = Field(..., ge=0)

    @validator('name')
    def name_must_not_be_blank(cls, v):
        if not v.strip():
            raise ValueError('Product name cannot be blank')
        return v.strip().title()

    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return round(v, 2)

    @validator('quantity')
    def quantity_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('Quantity cannot be negative')
        return v

    @validator('reorder_level')
    def reorder_level_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('Reorder level cannot be negative')
        return v

class ProductOut(BaseModel):
    pid: int
    name: str
    price: float
    quantity: int
    category_id: int
    reorder_level: int

    class Config:
        from_attributes = True