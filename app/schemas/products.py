from pydantic import BaseModel
from typing import Optional, List

# Base schema for creating/updating products
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity_at_stock: int
    is_active: Optional[bool] = True
    image_url: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None

# Schema for creating a product
class ProductCreate(ProductBase):
    pass

# Schema for updating a product
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None

# Schema for response
class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True
