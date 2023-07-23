# from fastapi import FastAPI
# from pydantic import BaseModel
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float

import datetime as _dt
import sqlalchemy as sqlalchemy 
import database as _database  
from sqlalchemy.orm import relationship, Mapped


class thirdparty_user_model(_database.Base):
    __tablename__ = "thirdparty_user"

    api_username = sqlalchemy.Column(sqlalchemy.String,primary_key=True, unique=True)
    api_password = sqlalchemy.Column(sqlalchemy.String)
    api_secret = sqlalchemy.Column(sqlalchemy.String)
