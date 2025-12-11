from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...schemas.orders import OrderCreate,OrderResponse
from ...crud.orders import create_order,OrderStatus
from ...database import get_db
from ...models import Order,PaymentStatus
from ...oauth import get_current_user
from ...crud.payments import start_payment_session
from ...schemas.payments import PaymentSessionResponse


router = APIRouter(
    prefix="/v1/payments",
    tags=["payments"]
)

@router.post("/checkout", response_model=PaymentSessionResponse)
def checkout(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # 1. Create order in DB
    new_order = create_order(db, current_user.id, order)

    # 2. Start payment session
    session_data = start_payment_session(new_order, current_user)

    return session_data


@router.post("/webhook")
async def payment_webhook(payload: dict, db: Session = Depends(get_db)):
    print("Webhook received:", payload)

    order_id = payload.get("order_id")
    payment_status = payload.get("status")

    if not order_id:
        return {"message": "order_id missing in payload"}

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return {"message": "Order not found"}

    if payment_status in ["PAID", "SUCCESS", "paid"]:
        order.payment_status = PaymentStatus.paid
        order.status = OrderStatus.processing
    elif payment_status in ["FAILED", "CANCELED", "failed"]:
        order.payment_status = PaymentStatus.failed
        order.status = OrderStatus.canceled

    db.commit()

    return {"message": "OK"}
