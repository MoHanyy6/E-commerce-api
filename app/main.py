from fastapi import FastAPI
from sqlalchemy.orm import Session
from . import models, schemas, utils, crud
from .database import engine, get_db
from .api.v1 import users, auth , products,orders ,payments,email_send

# Create tables
models.Base.metadata.create_all(bind=engine)
print("✅ Tables should now be created if they don’t exist.")

app = FastAPI()

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(payments.router)
# app.include_router(email_send.router)

@app.get("/")
async def home():
    return {"message": "work"}
