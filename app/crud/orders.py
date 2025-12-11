from sqlalchemy.orm import Session
from ..models import Order, OrderItem, Product, OrderStatus, PaymentStatus, ShippedStatus
from ..schemas.orders import OrderCreate
from fastapi import HTTPException, status
from datetime import datetime
import uuid

def create_order(db: Session, user_id: int, order_data: OrderCreate):

    # -------------------------------
    # 1️⃣ Validate product IDs + stock
    # -------------------------------
    products = {}
    total_price = 0.0

    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} not found"
            )

        if product.quantity_at_stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock for product '{product.name}'. Available: {product.quantity_at_stock}"
            )

        products[item.product_id] = product
        total_price += product.price * item.quantity

    # -------------------------------
    # 2️⃣ Create order
    # -------------------------------
    new_order = Order(
        user_id=user_id,
        address=order_data.address,
        total_price=total_price,
        status=OrderStatus.pending,
        payment_status=PaymentStatus.pending,
        shipped_status=ShippedStatus.not_shipped,
        tracking_number=str(uuid.uuid4())[:12],  # small tracking code
        created_at=datetime.utcnow()
    )

    db.add(new_order)
    db.flush()  # get new_order.id

    # -------------------------------
    # 3️⃣ Create order items AND reduce stock
    # -------------------------------
    for item in order_data.items:
        product = products[item.product_id]

        # Create order item
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=product.price
        )
        db.add(order_item)

        # Reduce stock
        product.quantity_at_stock -= item.quantity

    # -------------------------------
    # 4️⃣ Save order
    # -------------------------------
    db.commit()
    db.refresh(new_order)

    return new_order



def get_my_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()

# Get all orders (admin)
def get_all_orders(db: Session):
    return db.query(Order).all()

# Get single order by ID
def get_order_by_id(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order



def update_order_status(
    db: Session,
    order_id: int,
    status: str = None,
    payment_status: str = None,
    shipped_status: str = None
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update only provided fields
    if status:
        order.status = status
    if payment_status:
        order.payment_status = payment_status
    if shipped_status:
        order.shipped_status = shipped_status

    db.commit()
    db.refresh(order)
    return order