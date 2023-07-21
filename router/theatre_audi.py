from fastapi import Depends, APIRouter
from pydantic import BaseModel
from .base import get_db
from .auth import auth_class
from sqlalchemy.orm import session
import models
from fastapi.responses import JSONResponse




theatre_audi_router_and_seat_detail = APIRouter()
auth = auth_class()

def seat_detail(detail, db):

    
    # data construction 

    theatre_id = detail['theatre_id']
    audi_id = detail['audi_id']
    audi_name = detail['audi_name']
    audi_total_seat = detail['audi_total_seat']
    row = detail['row']
    column = detail['column']
    audi_seat_type = detail['audi_seat_type']


    total_seat_number = row * column

    seat_detail_data_json = []

    for i in range(row):
        row_character = chr(ord('A')+i)
        for j in range(column):

            seat_detail_model = models.seat_detail_model()
            
            column_number = j + 1
            seat_id = f"{row_character}{column_number}"
            print (seat_id)

            seat_name = f"{theatre_id}-{audi_id}-{audi_name}-{seat_id}"
            seat_name_without_space = seat_name.replace(" ","")

            seat_detail_model.seat_name = seat_name_without_space
            seat_detail_model.theatre_id = theatre_id
            seat_detail_model.seat_id = seat_id
            seat_detail_model.audi_id = audi_id
            seat_detail_model.row = row
            seat_detail_model.column = column
            seat_detail_model.is_active = True
            seat_detail_model.seat_type = audi_seat_type
            seat_detail_model.total_seat = total_seat_number 

            db.add(seat_detail_model)
            db.commit()

            
            single_seat_data = {
                "seat_name":seat_detail_model.seat_name,
                "theatre_id":seat_detail_model.theatre_id,
                "seat_id":seat_detail_model.seat_id,
                "audi_id":seat_detail_model.audi_id,
                "row":seat_detail_model.row,
                "column":seat_detail_model.column,
                "is_active":seat_detail_model.is_active,
                "seat_type":seat_detail_model.seat_type,
                "total_seat":seat_detail_model.total_seat
            }

            seat_detail_data_json.append(single_seat_data)

    
    return seat_detail_data_json



class threatre_audi_schema(BaseModel):
    audi_name: str
    audi_total_seat: int
    row: int
    column: int 
    audi_seat_type : str

@theatre_audi_router_and_seat_detail.post('/theatre_audi')
def theatre_audi(
        details:threatre_audi_schema, 
        db:session = Depends(get_db), 
        authenticate = Depends(auth.mid)
        ):

    theatre_audi_model = models.theatre_audi_model()

    theatre_audi_model.theatre_id = authenticate['theatre_id']
    theatre_audi_model.audi_name = details.audi_name
    theatre_audi_model.audi_total_seat = details.audi_total_seat
    theatre_audi_model.row = details.row
    theatre_audi_model.column = details.column
    theatre_audi_model.audi_seat_type = details.audi_seat_type

    db.add(theatre_audi_model)
    db.commit()

    db.refresh(theatre_audi_model)

    theatre_audi_data_json = {
        "theatre_id":authenticate['theatre_id'],
        "audi_id":theatre_audi_model.audi_id,
        "audi_name":details.audi_name,
        "audi_total_seat":details.audi_total_seat,
        "row":details.row,
        "column":details.column,
        "audi_seat_type":theatre_audi_model.audi_seat_type
    }

    seat_detail_data = seat_detail(theatre_audi_data_json, db)

    theatre_id = authenticate['theatre_id']
    return JSONResponse(content={
        "status":999,
        "audi_data":theatre_audi_data_json, 
        "seat_detail":seat_detail_data
    }, status_code=200)

    