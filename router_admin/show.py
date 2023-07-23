from fastapi import Depends, APIRouter
from pydantic import BaseModel
from .base import get_db
from .auth import auth_class
from sqlalchemy.orm import session
import models
from fastapi.responses import JSONResponse
from datetime import datetime


show_router = APIRouter()
auth = auth_class()

def show_seat_detail(detail, db):

    seat_detail_model = db.query(models.seat_detail_model).filter(models.seat_detail_model.theatre_id == detail['theatre_id'] and models.seat_detail_model.audi_id == detail['audi_id'])
    

    data = []

    if seat_detail_model is None:
        raise Exception 
    
    if seat_detail_model is not None:

        for i in seat_detail_model:

            show_seat_detail_model = models.show_seat_detail_model()

            show_seat_detail_model.show_id = detail['show_id'] 
            show_seat_detail_model.seat_name = i.seat_name + '-' + str(detail['show_id'])
            show_seat_detail_model.theatre_id = i.theatre_id 
            show_seat_detail_model.seat_id = i.seat_id 
            show_seat_detail_model.audi_id = i.audi_id 
            show_seat_detail_model.row = i.row 
            show_seat_detail_model.column = i.column 
            show_seat_detail_model.is_active = i.is_active 
            show_seat_detail_model.seat_type = i.seat_type 
            show_seat_detail_model.total_seat = i.total_seat 
            show_seat_detail_model.seat_status = i.seat_status
                
            db.add(show_seat_detail_model)
            db.commit()

            show_seat_detail_json = {
                "show_id":show_seat_detail_model.show_id,
                "seat_name":show_seat_detail_model.seat_name,
                "theatre_id":show_seat_detail_model.theatre_id,
                "seat_id":show_seat_detail_model.seat_id,
                "audi_id":show_seat_detail_model.audi_id,
                "row":show_seat_detail_model.row,
                "column":show_seat_detail_model.column,
                "is_active":show_seat_detail_model.is_active,
                "seat_type":show_seat_detail_model.seat_type,
                "total_seat":show_seat_detail_model.total_seat,
                "seat_status":show_seat_detail_model.seat_status
            }

            data.append(show_seat_detail_json)

        return data

        
class show_schema(BaseModel):
    movie_id : int 
    audi_id : int
    startTime : datetime
    show_status : str
    ticket_price : float

@show_router.post('/show')
def theatre_audi(
        details:show_schema, 
        db:session = Depends(get_db), 
        authenticate = Depends(auth.mid)
        ):

    show_model = models.show_model()

    movie_filtered = db.query(models.movie_model).filter(models.movie_model.movie_id == details.movie_id).first()
    audi_filtered = db.query(models.theatre_audi_model).filter(models.theatre_audi_model.audi_id == details.audi_id).first()

    if audi_filtered is not None:
        if movie_filtered is not None:
            if movie_filtered.theatre_id == authenticate['theatre_id']:
                if audi_filtered.audi_id == details.audi_id and audi_filtered.theatre_id == authenticate['theatre_id']:
                    if movie_filtered.movie_id == details.movie_id:

                        show_model.theatre_id = authenticate['theatre_id']
                        show_model.movie_id = details.movie_id
                        show_model.audi_id = details.audi_id
                        show_model.startTime = details.startTime
                        show_model.show_status = details.show_status
                        show_model.ticket_price = details.ticket_price

                        db.add(show_model)
                        db.commit()

                        db.refresh(show_model)

                        show_info_json = {
                            "theatre_id":authenticate['theatre_id'],
                            "movie_id":details.movie_id,
                            "audi_id":details.audi_id,
                            "show_id":show_model.show_id,
                            "startTime":str(details.startTime), 
                            "show_status":details.show_status,
                            "ticket_price":details.ticket_price
                        }

                        show_seat = show_seat_detail(show_info_json, db)
                        # theatre_id = authenticate['theatre_id']
                        return JSONResponse(content={
                            "status":999,
                            "show_info":show_info_json,
                            "seats":show_seat
                        }, status_code=200)

                    else:
                        return JSONResponse(content={
                            "error":"Movie ID mismatch.",
                            "status":999
                        }, status_code=400)
                else:
                    return JSONResponse(content={
                        "error":"Audi ID and theatre ID mismatch.",
                        "status":999
                    }, status_code=400)
            else:
                return JSONResponse(content={
                        "error":"Movie ID and theatre ID mismatch.",
                        "status":999
                    }, status_code=400)
        else:
            return JSONResponse(content={
                    "error":"Movie doesnot exists.",
                    "status":999
                }, status_code=400)
    else:
        return JSONResponse(content={
                "error":"AUDI doesnot exists.",
                "status":999
            }, status_code=400)