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


def seat_list(details, db):
    seat_detail_model = db.query(models.seat_detail_model).filter(models.seat_detail_model.theatre_id == details['theatre_id'] and models.seat_detail_model.audi_id == details['audi_id']).all()
    seat_hold_model = db.query(models.seat_hold_model).filter(models.seat_hold_model.show_id == details['show_id']).all()
    purchase_ticket_model = db.query(models.purchase_ticket_model).filter(models.purchase_ticket_model.show_id == details['show_id']).all()

    if seat_detail_model is None:
        return JSONResponse(content={
            "status":999, 
            "message":"seat not found"
        }, status_code=400)

    else:
        list_seat = []

        seat_hold_seat_names = {i.seat_name for i in seat_hold_model}
        purchase_ticket_seat_names = {i.seat_name for i in purchase_ticket_model}

        print (seat_hold_seat_names)
        print (purchase_ticket_seat_names)

        for i in seat_detail_model:
            if i.seat_name in seat_hold_seat_names:
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
                    "seat_status":int(4)
                }
                list_seat.append(single_seat)

            if i.seat_name in purchase_ticket_seat_names:
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
                    "seat_status":int(2)
                }
                list_seat.append(single_seat)

            else:
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
                    "seat_status":int(1)
                }
                list_seat.append(single_seat)

        return list_seat
    
 
class seat(BaseModel):
    theatre_id : int
    audi_id : int 
    movie_id : int 
    show_id : int 

@get_seat_router.post('/get_seat')
def get_seat(details : seat, db: Session = Depends(get_db), authenticate =Depends(auth.thirdparty_auth)):
    
    constructor_for_seat_list = {
            "theatre_id" : details.theatre_id,
            "audi_id" : details.audi_id,  
            "movie_id" : details.movie_id,  
            "show_id" : details.show_id  
            }
    list_of_seat = seat_list(constructor_for_seat_list, db)

    return JSONResponse(content={
        "status":000,
        "data": list_of_seat
    }, status_code=200)

    

