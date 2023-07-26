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


class show_schema(BaseModel):
    movie_id: int
    audi_id: int
    startTime: datetime
    show_status: str
    ticket_price: float


@show_router.post("/show")
def show_create(
    details: show_schema, db: session = Depends(get_db), authenticate=Depends(auth.mid)
):
    show_model = models.show_model()

    movie_filtered = (
        db.query(models.movie_model)
        .filter(models.movie_model.movie_id == details.movie_id)
        .first()
    )
    audi_filtered = (
        db.query(models.theatre_audi_model)
        .filter(models.theatre_audi_model.audi_id == details.audi_id)
        .first()
    )

    if audi_filtered is not None:
        if movie_filtered is not None:
            if movie_filtered.theatre_id == authenticate["theatre_id"]:
                if (
                    audi_filtered.audi_id == details.audi_id
                    and audi_filtered.theatre_id == authenticate["theatre_id"]
                ):
                    if movie_filtered.movie_id == details.movie_id:
                        show_model.theatre_id = authenticate["theatre_id"]
                        show_model.movie_id = details.movie_id
                        show_model.audi_id = details.audi_id
                        show_model.startTime = details.startTime
                        show_model.show_status = details.show_status
                        show_model.ticket_price = details.ticket_price

                        db.add(show_model)
                        db.commit()

                        db.refresh(show_model)

                        show_info_json = {
                            "theatre_id": authenticate["theatre_id"],
                            "movie_id": details.movie_id,
                            "audi_id": details.audi_id,
                            "show_id": show_model.show_id,
                            "startTime": str(details.startTime),
                            "show_status": details.show_status,
                            "ticket_price": details.ticket_price,
                        }

                        return JSONResponse(
                            content={"status": 999, "show_info": show_info_json},
                            status_code=200,
                        )

                    else:
                        return JSONResponse(
                            content={"error": "Movie ID mismatch.", "status": 999},
                            status_code=400,
                        )
                else:
                    return JSONResponse(
                        content={
                            "error": "Audi ID and theatre ID mismatch.",
                            "status": 999,
                        },
                        status_code=400,
                    )
            else:
                return JSONResponse(
                    content={
                        "error": "Movie ID and theatre ID mismatch.",
                        "status": 999,
                    },
                    status_code=400,
                )
        else:
            return JSONResponse(
                content={"error": "Movie doesnot exists.", "status": 999},
                status_code=400,
            )
    else:
        return JSONResponse(
            content={"error": "AUDI doesnot exists.", "status": 999}, status_code=400
        )
