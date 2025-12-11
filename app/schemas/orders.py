from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    
class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: float
class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    address: str

class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    payment_status: str
    shipped_status: str
    address: str
    total_price: float
    tracking_number: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    shipped_at: Optional[datetime]
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
