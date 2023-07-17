from fastapi import APIRouter, Form, Depends
from fastapi import FastAPI
# import models
import models
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
# from database import SessionLocal
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import jwt
# from ...task_manager.main import get_db


auth_router = APIRouter()
app = FastAPI()

SECRET_KEY = "1111"
ALGORITHM = "HS256"


class auth_class():
    def create_access_token(self, raw_data:dict):
        expire = datetime.utcnow() + timedelta(minutes=100)
        raw_data.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(raw_data, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

