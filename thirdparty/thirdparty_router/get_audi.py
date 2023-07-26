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

get_theatre_audi_router = APIRouter()


class theatre_audi(BaseModel):
    theatre_id: int


@get_theatre_audi_router.post("/theatre_audi")
def get_theatre_list(
    details: theatre_audi,
    db: Session = Depends(get_db),
    authenticate=Depends(auth.thirdparty_auth),
):
    theatre_audi_model = db.query(models.theatre_audi_model).filter(
        models.theatre_audi_model.theatre_id == details.theatre_id
    )
    list_audi = []

    if theatre_audi_model is None:
        return JSONResponse(
            content={
                "status": 999,
                "message": f"Theatre with {details['theatre_id']} not found",
            },
            status_code=400,
        )

    for i in theatre_audi_model:
        single_audi = {
            "audi_id": i.audi_id,
            "audi_name": i.audi_name,
            "audi_total_seat": i.audi_total_seat,
            "row": i.row,
            "column": i.column,
            "audi_seat_type": i.audi_seat_type,
        }

        list_audi.append(single_audi)

    return JSONResponse(content={"status": 000, "data": list_audi}, status_code=200)
