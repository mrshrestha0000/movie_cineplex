from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models
import database

from router_admin.auth import auth_router
from router_admin.create_token import token_router
from router_admin.theatre_info_and_auth import add_theatre_and_create_auth_data_router
from router_admin.theatre_audi import theatre_audi_router_and_seat_detail
from router_admin.movie_info import movie_router
from router_admin.show import show_router
from router_admin.create_thirdparty_user import create_thirdparty_user_router

from thirdparty.thirdparty_router.thirdparty_token import thirdparty_token_router
from thirdparty.thirdparty_router.get_theatre import get_theatre_list_router
from thirdparty.thirdparty_router.get_audi import get_theatre_audi_router
from thirdparty.thirdparty_router.get_movie import get_movie_router
from thirdparty.thirdparty_router.get_show import get_show_router
from thirdparty.thirdparty_router.get_seat import get_seat_router
from thirdparty.thirdparty_router.seat_hold import seat_hold_router
from thirdparty.thirdparty_router.purchase_ticket import purchase_ticket_router


app = FastAPI(debug=True)

app.include_router(token_router, prefix="/auth")
app.include_router(add_theatre_and_create_auth_data_router, prefix="/admin")
app.include_router(theatre_audi_router_and_seat_detail, prefix="/admin")
app.include_router(movie_router, prefix="/admin")
app.include_router(show_router, prefix="/admin")
app.include_router(create_thirdparty_user_router, prefix="/admin")


app.include_router(thirdparty_token_router, prefix="/thirdparty")
app.include_router(get_theatre_list_router, prefix="/thirdparty")
app.include_router(get_theatre_audi_router, prefix="/thirdparty")
app.include_router(get_movie_router, prefix="/thirdparty")
app.include_router(get_show_router, prefix="/thirdparty")
app.include_router(get_seat_router, prefix="/thirdparty")
app.include_router(seat_hold_router, prefix="/thirdparty")
app.include_router(purchase_ticket_router, prefix="/thirdparty")


database.Base.metadata.create_all(bind=engine)
