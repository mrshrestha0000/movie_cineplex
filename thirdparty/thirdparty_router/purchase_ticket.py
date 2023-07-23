# from fastapi import Depends, APIRouter, HTTPException
# from pydantic import BaseModel
# from router_admin.base import get_db
# from router_admin.auth import auth_class
# from sqlalchemy.orm import session
# import models
# from fastapi.responses import JSONResponse
# from datetime import datetime, timedelta


# purchase_ticket_router = APIRouter()
# auth = auth_class()


# class purchase_ticket_schema(BaseModel):

#     show_id : int 
#     seat_name : list 
#     transaction_id : str 

# @purchase_ticket_router.post('/purchase_ticket')
# def seat_hold(details : purchase_ticket_schema, 
#               db:session = Depends(get_db),
#               authenticate = Depends(auth.thirdparty_auth)):
#     try: 

#         show_id=details.show_id
#         transaction_id=details.transaction_id
#         seat_name=details.seat_name

#         selected_seat = []

#         seat_available = validate_seat_avaibility(seat_name, db)

#         for i in range(len(seat_name)):
        
#             show_seat_detail_model = db.query(models.show_seat_detail_model).filter(models.show_seat_detail_model.seat_name == seat_name[i]).first()
#             show_model = db.query(models.show_model).filter(models.show_model.show_id == show_id).first()
#             seat_hold_model = models.seat_hold_model()

#             if show_seat_detail_model is None:
#                 return JSONResponse(content={
#                     "error":"Inavlid seat name",
#                     "status":999
#                 }, status_code=400)
            
#             if show_model is None:
#                 return JSONResponse(content={
#                     "status":999,
#                     "error":"Invalid show id."
#                 }, status_code=400)
            
#             if show_seat_detail_model is not None:
#                 # if show_seat_detail_model.seat_status == 1:
#                 current_datetime = datetime.now()
#                 seat_hold_expire_datetime = current_datetime + timedelta(minutes = 10)
                
#                 seat_hold_model.show_id = show_id
#                 seat_hold_model.seat_name = seat_name[i]
#                 seat_hold_model.exipry_time = seat_hold_expire_datetime
#                 seat_hold_model.transaction_id = transaction_id

#                 seat_hold_json = {
#                     "seat_name": seat_hold_model.seat_name,
#                     "show_id": show_id,
#                     "seat_hold_expire_datetime": seat_hold_expire_datetime,
#                     "transaction_id":transaction_id
#                 }

#                 selected_seat.append(seat_name[i])

#                 db.add(seat_hold_model)
#                 db.commit()

#                 seat_hold_from_audi(seat_hold_json, db)
                
#         return JSONResponse(content={
#             "status":999,
#             "seat_name":selected_seat, 
#             "message":"seat hold success."
#         }, status_code=200)

#     except Exception as e:
#         # import pdb ; pdb.set_trace()

#         return JSONResponse(content={
#                 "error":e.detail,
#                 "status":999
#             }, status_code=400)



