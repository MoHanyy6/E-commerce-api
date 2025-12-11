from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship
from .database import Base
import enum
import uuid

# ------------------------
# Enums
# ------------------------
class UserRole(str, enum.Enum):
    admin = "admin"
    customer = "customer"

class OrderStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    canceled = "canceled"
    processing = "processing" 
    
class PaymentStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed" 

class ShippedStatus(str, enum.Enum):
    not_shipped = "not_shipped"
    shipped = "shipped"
    delivered = "delivered"


# ------------------------
# Order Item Model
# ------------------------
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price_at_purchase = Column(Float, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


# ------------------------
# User Model
# ------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.customer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, default=lambda: str(uuid.uuid4()))
    code_expires_at = Column(DateTime, nullable=True)
    verification_attempts = Column(Integer, default=0)

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")


# ------------------------
# Product Model
# ------------------------
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    quantity_at_stock = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    image_url = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    category = Column(String, nullable=True)

    order_items = relationship("OrderItem", back_populates="product")


# ------------------------
# Order Model
# ------------------------
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)
    shipped_status = Column(Enum(ShippedStatus), default=ShippedStatus.not_shipped, nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.pending, nullable=False)
    address = Column(String, nullable=False)
    total_price = Column(Float, nullable=False, default=0.0)
    tracking_number = Column(String, nullable=True)
    delivery_date_estimate = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    shipped_at = Column(DateTime(timezone=True), nullable=True)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    user = relationship("User", back_populates="orders")
