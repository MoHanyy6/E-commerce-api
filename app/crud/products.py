from sqlalchemy.orm import Session
from ..models import Product
from ..schemas.products import ProductCreate, ProductUpdate

from typing import List, Optional

# Create product
def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Get single product by id
def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

# Get all products with optional filters
def get_products(
    db: Session,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None
) -> List[Product]:
    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    if tag:
        query = query.filter(Product.tags.like(f"%{tag}%"))
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    return query.all()

# Update product
def update_product(db: Session, product_id: int, update_data: ProductUpdate):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

# Delete product
def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    db.delete(product)
    db.commit()
    return product
