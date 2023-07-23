from fastapi import Depends, APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from router_admin.auth import auth_router
from database import SessionLocal, engine
from sqlalchemy.orm import Session

import models
import database
from router_admin.auth import auth_class
from router_admin.base import get_db
from thirdparty.thirdparty_models import thirdparty_models
from datetime import datetime

auth = auth_class()

get_seat_router = APIRouter()
 
class seat(BaseModel):
    theatre_id : int
    audi_id : int 
    movie_id : int 
    show_id : int 

@get_seat_router.post('/get_seat')
def get_seat(details : seat, db: Session = Depends(get_db), authenticate =Depends(auth.thirdparty_auth)):
    
    seat_detail_model = db.query(models.show_seat_detail_model).filter(models.show_seat_detail_model.theatre_id == details.theatre_id and models.show_seat_detail_model.audi_id == details.audi_id and models.show_seat_detail_model.movie_id == details.movie_id and models.show_seat_detail_model.show_id == details.show_id)
    
    # theatre_id = details.theatre_id

    if seat_detail_model is None:
        return JSONResponse(content={
            "status":999, 
            "message":"seat not found"
        }, status_code=400)

    else:
        list_seat = []
        for i in seat_detail_model:

            single_seat = {
                "seat_name":i.seat_name,
                "theatre_id":i.theatre_id,
                "seat_id":i.seat_id,
                "audi_id":i.audi_id,
                "row":i.row,
                "column":i.column,
                "is_active":i.is_active,
                "seat_type":i.seat_type,
                "total_seat":i.total_seat,
                "seat_status":i.seat_status
            }

            list_seat.append(single_seat)

        return JSONResponse(content={
            "status":000,
            "data": list_seat
        }, status_code=200)

    

