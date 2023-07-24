from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from router_admin.base import get_db
from router_admin.auth import auth_class
from sqlalchemy.orm import session
import models
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
# from seat_hold import seat_hold_details_function
from thirdparty.thirdparty_router.seat_hold import seat_hold_details_function
from router_admin.create_thirdparty_user import generate_random_alphanumeric

purchase_ticket_router = APIRouter()
auth = auth_class()


def seat_book_from_audi(details, db):
    # seat_detail_model = models.seat_detail_model()
    selected_seat_instance = db.query(models.show_seat_detail_model).filter(models.show_seat_detail_model.seat_name == details).first()
    try: 
        if selected_seat_instance is not None:
            print (selected_seat_instance.seat_status)
            if selected_seat_instance.seat_status == 1 or selected_seat_instance.seat_status == 4:
                selected_seat_instance.seat_status = int(2)

                db.add(selected_seat_instance)
                db.commit()

            else:
                raise HTTPException(status_code=400, detail="Cannot purchase ticket because seat is already booked.")               

    except Exception as e:
        raise HTTPException(status_code=400, detail="Cannot purchase ticket.")               

    
# show_id
# seat_name
# transaction_id
# api_username
def purchase_ticket_validation(details , db):
    purchase_ticket_model = db.query(models.purchase_ticket_model).filter(models.purchase_ticket_model.show_id == details['show_id']).all()
    purchase_ticket_model_filter_by_api_username = db.query(models.purchase_ticket_model).filter(models.purchase_ticket_model.api_username == details['api_username']).all()
    for i in purchase_ticket_model:
        print (details['seat_name'])
        print (i.seat_name)
        if details['seat_name'] == i.seat_name:
            
            raise HTTPException(status_code=400, detail="Seat already purchased.")   
        for j in purchase_ticket_model_filter_by_api_username:
            print (details['transaction_id'])
            print (j.transaction_id)
            if str(details['transaction_id']) == str(j.transaction_id):
                raise HTTPException(status_code=400, detail="Duplicate transaction_id")   
            
        return True





class purchase_ticket_schema(BaseModel):
    show_id : int 
    seat_name : list 
    transaction_id : str 
    amount : float

@purchase_ticket_router.post('/purchase_ticket')
def purchase_ticket(details : purchase_ticket_schema, 
              db:session = Depends(get_db),
              authenticate = Depends(auth.thirdparty_auth)):
    try: 
        seat_hold_data = seat_hold_details_function(authenticate, details, db)
        purchase_ticket_model = models.purchase_ticket_model()
        show_model = db.query(models.show_model).filter(models.show_model.show_id == details.show_id).first()
        theatre_id = show_model.theatre_id
        theatre_info_model = db.query(models.theatre_info_model).filter(models.theatre_info_model.theatre_id == theatre_id).first()
        show_model = db.query(models.show_model).filter(models.show_model.show_id == details.show_id).first()
        audi_id = show_model.audi_id
        theatre_audi_model = db.query(models.theatre_audi_model).filter(models.theatre_audi_model.audi_id == audi_id).first()
        movie_model = db.query(models.movie_model).filter(models.movie_model.movie_id == show_model.movie_id).first()

        amount = 0 
        for i in seat_hold_data:
            amount = i['ticket_price'] + amount
        
        if details.amount == amount:
            ticket_detail = []

            for j in seat_hold_data:
                validate_ticket_purhase_json = {
                    "show_id":details.show_id,
                    "seat_name":j['seat_name'],
                    "transaction_id":details.transaction_id,
                    "api_username":authenticate['api_username']
                }

                validate_ticket_purhase_model = purchase_ticket_validation(validate_ticket_purhase_json, db)

                purchase_ticket_model.amount = j['ticket_price']
                purchase_ticket_model.transaction_id = details.transaction_id
                purchase_ticket_model.seat_name = j['seat_name']
                purchase_ticket_model.api_username = authenticate['api_username']
                purchase_ticket_model.audi_id = show_model.audi_id
                purchase_ticket_model.show_id = j['show_id']
                a = j['seat_name']
                seat_book_from_audi(a, db)

                db.add(purchase_ticket_model)
                db.commit()

                db.refresh(purchase_ticket_model)
                ticket_id = purchase_ticket_model.ticket_id

                single_ticket_details = {
                    "ticket_id":ticket_id,
                    "theatre_name":theatre_info_model.theatre_name,
                    "location_name":theatre_info_model.location_name,
                    "audi_name":theatre_audi_model.audi_name, 
                    "movie_name":movie_model.movie_name,
                    "movie_type":movie_model.movie_type,
                    "duration":movie_model.duration,
                    "show_date":str(show_model.startTime),
                    "ticket_price":show_model.ticket_price,
                    "seat_name":j['seat_name']
                }

                ticket_detail.append(single_ticket_details)


            return JSONResponse(content={
                "transaction_id":details.transaction_id,
                "status":000,
                "message":"Ticket_purchase_successful.",
                "tickets":ticket_detail
            }, status_code=200)
        else:
            return JSONResponse(content={
                "message":"amount mismatch.",
                "status":999
            })

    except Exception as e:
        return JSONResponse(content={
            "error":str(e),
            "detail":e.detail,
            "status":999
        }, status_code=400)


