from pydantic import BaseModel, validator, Field

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)

    @validator('name')
    def name_must_not_be_blank(cls, v):
        if not v.strip():
            raise ValueError('Category name cannot be blank')
        return v.strip().title()

class CategoryOut(BaseModel):
    cid: int
    name: str

    class Config:
        from_attributes = True