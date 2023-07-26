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

get_show_router = APIRouter()


class theatre_show(BaseModel):
    theatre_id: int
    movie_id: int


@get_show_router.post("/get_show")
def get_movie(
    details: theatre_show,
    db: Session = Depends(get_db),
    authenticate=Depends(auth.thirdparty_auth),
):
    show_model = db.query(models.show_model).filter(
        models.show_model.theatre_id == details.theatre_id
        and models.show_model.movie_id == details.movie_id
    )

    theatre_id = details.theatre_id

    if show_model is None:
        return JSONResponse(
            content={"status": 999, "message": "Show not found"}, status_code=400
        )

    else:
        list_show = []
        for i in show_model:
            time = i.startTime
            show_date = str(time.date())

            time_component = time.time()
            time_in_ampm_format = time_component.strftime("%I:%M:%S %p")

            single_movie = {
                "movie_id": i.movie_id,
                "audi_id": i.audi_id,
                "show_id": i.show_id,
                "show_date": show_date,
                "show_time": time_in_ampm_format,
                "show_status": i.show_status,
                "ticket_price": i.ticket_price,
            }

            list_show.append(single_movie)

        return JSONResponse(content={"status": 000, "data": list_show}, status_code=200)
