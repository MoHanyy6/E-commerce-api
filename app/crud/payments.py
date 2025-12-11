import requests
from sqlalchemy.orm import Session
from ..models import Order
from ..schemas.payments import PaymentSessionResponse



PAYMENT_GATEWAY_URL = "https://example.com/api/payments/create"  # replace with gateway URL

def start_payment_session(order: Order, user):
    payload = {
        "merchantRefNumber": order.id,
        "amount": order.total_price,
        "currency": "EGP",
        "customer": {
            "id": user.id,
            "email": user.email
        },
        "success_url": "https://yourdomain.com/payment/success",
        "failure_url": "https://yourdomain.com/payment/failed"
    }

    response = requests.post(PAYMENT_GATEWAY_URL, json=payload)
    data = response.json()

    return {
        "order_id": order.id,
        "payment_url": data.get("payment_url")  # gateway returns a URL
    }