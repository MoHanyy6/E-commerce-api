from fastapi import FastAPI , Query, Path,Body,status,HTTPException,Depends,APIRouter
from typing import List,Optional
from random import randrange
import psycopg
# from psycopg import RealDictCursor
from .. import models,schemas,utils,oauth
from sqlalchemy.orm import Session
from ..database import engine,get_db
from sqlalchemy import func
from ..schemas.users import UserCreate, UserResponse

def get_users(db: Session ,skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()



def get_user_by_email(email: str ,db: Session):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    hashed_pw = utils.hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(user_id:int,db: Session= Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user