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

auth = auth_class()

get_theatre_list_router = APIRouter()
 
@get_theatre_list_router.get('/theatre_list')
def get_theatre_list(db: Session = Depends(get_db), authenticate =Depends(auth.thirdparty_auth)):
    # theatre_info_model = models.theatre_info_model.all()
    theatre_info_model = db.query(models.theatre_info_model).all()
    list_theatre = []

    for i in theatre_info_model:
        single_theatre = {
            "theatre_id":i.theatre_id,
            "theatre_code":i.theatre_code,
            "theatre_name":i.theatre_name,
            "location_id":i.location_id,
            "location_name":i.location_name,
            "address":i.address,
            "vat_number":i.vat_number,
            "contact":i.contact
        }

        list_theatre.append(single_theatre)

    return JSONResponse(content={
        "status":000,
        "data": list_theatre
    }, status_code=200)

    

