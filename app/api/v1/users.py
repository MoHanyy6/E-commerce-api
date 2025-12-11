from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from ... import models, utils, dependencies,oauth,schemas
from ...database import get_db
from ...crud import users
from ...schemas.users import UserResponse,UserCreate  # Import your response schema
from ...dependencies import require_role

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100,
              db: Session = Depends(get_db),  
            current_user: models.User = Depends(require_role("admin"))):
            
    return users.get_users(db, skip=skip, limit=limit)

@router.get("/by_email", response_model=UserResponse)
def get_user_by_email(
    user_email: str = Query(..., description="Email of the user to fetch"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("admin"))
):
    user = users.get_user_by_email(user_email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with email {user_email} was not found"
        )
    return user

# @router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
# def create_new_user(user: UserCreate, db: Session = Depends(get_db),  
#             current_user: models.User = Depends(require_role("admin"))):
#     existing_user = users.get_user_by_email(user.email, db)
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return users.create_user(user, db)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(
    user: UserCreate, 
    db: Session = Depends(get_db),  
    current_user: models.User = Depends(require_role("admin"))
):
    existing_user = users.get_user_by_email(user.email, db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user directly with is_verified=True
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=utils.hash(user.password),
        role=user.role if user.role else "customer",  # optional
        is_verified=True  # ✅ bypass verification
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user





@router.delete("/")
def delete_user(user_id: int, db: Session = Depends(get_db),  
            current_user: models.User = Depends(require_role("admin"))):
    deleted_user = users.delete_user(user_id=user_id, db=db)
    
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully", "user_id": user_id}
