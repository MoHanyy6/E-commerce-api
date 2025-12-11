from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# from schemas.products import ProductCreate, ProductUpdate, ProductResponse
from ...schemas.products import ProductCreate, ProductUpdate, ProductResponse
from ...crud import products as crud_product
from ...database import get_db
from ...models import User
from ...dependencies import require_role

router = APIRouter(prefix="/v1/products", tags=["Products"])

# Create product
@router.post("/", response_model=ProductResponse)
def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db),  
            current_user: User = Depends(require_role("admin"))):
    return crud_product.create_product(db, product)

# Get single product
@router.get("/{product_id}", response_model=ProductResponse)
def get_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    product = crud_product.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Get all products with optional filters
@router.get("/", response_model=List[ProductResponse])
def get_products_endpoint(
    category: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return crud_product.get_products(db, category, tag, search)

# Update product
@router.put("/{product_id}", response_model=ProductResponse)
def update_product_endpoint(product_id: int, update_data: ProductUpdate, db: Session = Depends(get_db)):
    product = crud_product.update_product(db, product_id, update_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Delete product
@router.delete("/{product_id}", response_model=ProductResponse)
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db),  
        current_user: User = Depends(require_role("admin"))):
    product = crud_product.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
