from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime



class PaymentSessionResponse(BaseModel):
    order_id: int
    payment_url: str