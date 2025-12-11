# from passlib.context import CryptContext


# pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

# def hash(password):
#     password=password[:70]
#     return pwd_context.hash(password)

# def verify(plain_password,hashed_password):
#     return pwd_context.verify(plain_password,hashed_password)

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str) -> str:
    # Convert to bytes and truncate to 72 bytes
    password = password.encode("utf-8")[:72]
    return pwd_context.hash(password)

def verify(plain_password: str, hashed_password: str) -> bool:
    # Also truncate bytes when verifying
    plain_bytes = plain_password.encode("utf-8")[:72]
    return pwd_context.verify(plain_bytes, hashed_password)
