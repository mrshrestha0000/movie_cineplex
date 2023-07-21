from fastapi import FastAPI , Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models
import database

from router.auth import auth_router
from router.create_token import token_router
from router.theatre_info_and_auth import add_theatre_and_create_auth_data_router
from router.theatre_audi import theatre_audi_router_and_seat_detail
from router.movie_info import movie_router
from router.show import show_router


app = FastAPI(debug=True)

app.include_router(token_router, prefix='/auth')
app.include_router(add_theatre_and_create_auth_data_router, prefix='/v1')
app.include_router(theatre_audi_router_and_seat_detail, prefix="/v1")
app.include_router(movie_router, prefix="/v1")
app.include_router(show_router, prefix="/v1")
# app.include_router(seat_detail_router, prefix="/v1")

database.Base.metadata.create_all(bind=engine)