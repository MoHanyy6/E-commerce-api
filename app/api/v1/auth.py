from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ... import database, models, utils, oauth
from ...schemas.users import Token,UserCreate,UserRegister  # Correct import for Token schema
from uuid import uuid4
from ...send_email import send_email
from ...database import get_db
from uuid import uuid4
from datetime import datetime, timedelta
import random
from pydantic import EmailStr
router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

# @router.post("/register", status_code=201)
# async def register(user: UserRegister, db: Session = Depends(get_db)):

#     # Check if email exists
#     existing = db.query(models.User).filter(models.User.email == user.email).first()
#     if existing:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     # Force role to "customer" for this endpoint
#     default_role = "customer"

#     # Generate verification token
#     verification_token = str(uuid4())

#     new_user = models.User(
#         name=user.name,
#         email=user.email,
#         hashed_password=utils.hash(user.password),
#         role=default_role,  # ignore whatever user.role contains
#         is_verified=False,
#         verification_token=verification_token
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     # Prepare verification email
#     verify_link = f"http://127.0.0.1:8000/api/v1/auth/verify?token={verification_token}"
#     body = f"""
#     <h2>Verify your email</h2>
#     <p>Click the link below to verify your account:</p>
#     <a href="{verify_link}">Verify Email</a>
#     """

#     await send_email(
#         email_to=new_user.email,
#         subject="Verify your email",
#         body=body
#     )

#     return {"message": "Check your email to verify your account"}


# @router.get("/verify")
# def verify_email(token: str, db: Session = Depends(database.get_db)):

#     user = db.query(models.User).filter(
#         models.User.verification_token == token
#     ).first()

#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid token")

#     user.is_verified = True
#     user.verification_token = None

#     db.commit()

#     return {"message": "Email verified successfully"}

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", status_code=201)
async def register(user: UserRegister, db: Session = Depends(database.get_db)):

    # Check if email already exists
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Generate 6-digit verification code
    verification_code = str(random.randint(100000, 999999))

    # Code expires after 15 minutes
    expires_at = datetime.utcnow() + timedelta(minutes=15)

    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=utils.hash(user.password),
        role="customer",
        is_verified=False,
        verification_token=verification_code,
        code_expires_at=expires_at
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Email content
    body = f"""
    <h2>Email Verification</h2>
    <p>Your verification code is:</p>
    <h1>{verification_code}</h1>
    <p>This code will expire in 15 minutes.</p>
    """

    await send_email(
        email_to=new_user.email,
        subject="Verify your email",
        body=body
    )

    return {"message": "Verification code sent to your email"}


@router.post("/verify-code")
def verify_code(email: str, code: str, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "Account already verified"}

    # ✅ BLOCK AFTER TOO MANY ATTEMPTS
    if user.verification_attempts >= 5:
        raise HTTPException(
            status_code=403,
            detail="Too many attempts. Please request a new code."
        )

    # ✅ CHECK EXPIRY
    if not user.code_expires_at or user.code_expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Verification code expired"
        )

    # ✅ WRONG CODE
    if user.verification_token != code:
        user.verification_attempts += 1
        db.commit()
        raise HTTPException(status_code=400, detail="Invalid verification code")

    # ✅ SUCCESS
    user.is_verified = True
    user.verification_token = None
    user.code_expires_at = None
    user.verification_attempts = 0

    db.commit()

    return {"message": "Email verified successfully"}


@router.post("/resend-code")
async def resend_code(email: EmailStr, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "Account already verified"}

    user.verification_token = str(random.randint(100000, 999999))
    user.code_expires_at = datetime.utcnow() + timedelta(minutes=15)
    user.verification_attempts = 0

    db.commit()

    await send_email(
        email_to=user.email,
        subject="Your new verification code",
        body=f"<h1>{user.verification_token}</h1>"
    )

    return {"message": "Verification code resent"}




@router.post("/login", response_model=Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user or not utils.verify(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Please verify your email before logging in"
        )

    

    access_token = oauth.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
