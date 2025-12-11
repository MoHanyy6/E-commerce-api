from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...schemas.orders import OrderCreate,OrderResponse
from ...crud.orders import create_order,get_my_orders,get_all_orders,get_order_by_id,update_order_status
from ...database import get_db
from ...models import Order,Product,User
from ...oauth import get_current_user
from...send_email import send_email
from ...dependencies import require_role
import asyncio

router = APIRouter(
    prefix="/v1/orders",
    tags=["orders"]
)

@router.post("/", response_model=OrderResponse)
async def create_order_endpoint(order: OrderCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    new_order = create_order(db, current_user.id, order)

    # Prepare order items table in HTML
    order_items_html = ""
    order_total = 0
    for item in new_order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        price = product.price * item.quantity
        order_total += price
        order_items_html += f"""
        <tr>
            <td>{product.name}</td>
            <td>{item.quantity}</td>
            <td>${product.price}</td>
            <td>${price}</td>
        </tr>
        """

    body = f"""
    <h2>Hi {current_user.name},</h2>
    <p>Thank you for your order #{new_order.id}!</p>
    <table border="1" cellpadding="5" cellspacing="0">
        <tr>
            <th>Product</th><th>Quantity</th><th>Price</th><th>Total</th>
        </tr>
        {order_items_html}
        <tr>
            <td colspan="3"><b>Order Total</b></td>
            <td>${order_total}</td>
        </tr>
    </table>
    <p>Shipping Address: {new_order.address}</p>
    """

    # Send email in background
    asyncio.create_task(send_email(
        email_to=current_user.email,
        subject=f"Order Confirmation #{new_order.id}",
        body=body
    ))

    return new_order
    

# -------------------------------
# List all orders endpoint
# -------------------------------
@router.get("/", response_model=List[OrderResponse])
def list_orders(db: Session = Depends(get_db),current_user = Depends(require_role("admin"))):
    return get_all_orders(db)






@router.get("/my",response_model=List[OrderResponse])
def get_my_orders_endpoint(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_my_orders(db, current_user.id)


# -------------------------------
# Get single order by ID
# -------------------------------
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return get_order_by_id(db, order_id)



# -------------------------------
# Update order status (admin only)
# -------------------------------
@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status_endpoint(
    order_id: int,
    status: str = None,
    payment_status: str = None,
    shipped_status: str = None,
    db: Session = Depends(get_db),  
    current_user: User = Depends(require_role("admin"))
):
    
    return update_order_status(db, order_id, status, payment_status, shipped_status)