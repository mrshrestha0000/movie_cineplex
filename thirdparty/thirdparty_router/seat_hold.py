from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from router_admin.base import get_db
from router_admin.auth import auth_class
from sqlalchemy.orm import session
import models
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from thirdparty.thirdparty_models import thirdparty_models
from thirdparty.thirdparty_router.get_seat import seat_list

seat_hold_router = APIRouter()
auth = auth_class()


def validate_seat_avaibility(details, seat_name: list, db, authenticate):
    for i in range(len(seat_name)):
        list_of_seat = seat_list(details, db)
        seat_hold_model = (
            db.query(models.seat_hold_model)
            .filter(models.seat_hold_model.transaction_id == details["transaction_id"])
            .all()
        )

        for i in seat_hold_model:
            if i.api_username == authenticate["api_username"]:
                raise HTTPException(status_code=400, detail="Duplicate txn id.")

        a = []
        for j in list_of_seat:
            if seat_name[i] == j["seat_name"]:
                if (
                    j["seat_status"] == int(2)
                    or j["seat_status"] == int(3)
                    or j["seat_status"] == int(4)
                ):
                    raise HTTPException(
                        status_code=400, detail="Seat cannot be selected."
                    )
                if j["seat_status"] == int(1):
                    a.append(j["seat_name"])

        if a == []:
            raise HTTPException(status_code=400, detail="Seat name not found")

        else:
            return True


class seat_hold_schema(BaseModel):
    show_id: int
    seat_name: list
    transaction_id: str


@seat_hold_router.post("/seat_hold")
def seat_hold(
    details: seat_hold_schema,
    db: session = Depends(get_db),
    authenticate=Depends(auth.thirdparty_auth),
):
    try:
        show_id = details.show_id
        transaction_id = details.transaction_id
        seat_name = details.seat_name

        show_model = (
            db.query(models.show_model)
            .filter(models.show_model.show_id == show_id)
            .first()
        )
        selected_seat = []

        if show_model is None:
            return JSONResponse(
                content={"status": 999, "error": "Invalid show id."}, status_code=400
            )

        constructor_for_seat_list = {
            "theatre_id": show_model.theatre_id,
            "audi_id": show_model.audi_id,
            "movie_id": show_model.movie_id,
            "show_id": show_model.show_id,
            "transaction_id": details.transaction_id,
        }

        seat_available = validate_seat_avaibility(
            constructor_for_seat_list, seat_name, db, authenticate
        )

        for i in range(len(seat_name)):
            seat_detail_model = (
                db.query(models.seat_detail_model)
                .filter(models.seat_detail_model.seat_name == seat_name[i])
                .first()
            )
            show_model = (
                db.query(models.show_model)
                .filter(models.show_model.show_id == show_id)
                .first()
            )
            seat_hold_model = models.seat_hold_model()

            if seat_detail_model is None:
                return JSONResponse(
                    content={"error": "Inavlid seat name", "status": 999},
                    status_code=400,
                )

            if seat_detail_model is not None:
                current_datetime = datetime.now()
                seat_hold_expire_datetime = current_datetime + timedelta(minutes=10)

                seat_hold_model.show_id = show_id
                seat_hold_model.seat_name = seat_name[i]
                seat_hold_model.exipry_time = seat_hold_expire_datetime
                seat_hold_model.transaction_id = transaction_id
                seat_hold_model.api_username = authenticate["api_username"]

                seat_hold_json = {
                    "seat_name": seat_hold_model.seat_name,
                    "show_id": show_id,
                    "seat_hold_expire_datetime": seat_hold_expire_datetime,
                    "transaction_id": transaction_id,
                }

                selected_seat.append(seat_name[i])

                db.add(seat_hold_model)
                db.commit()

        return JSONResponse(
            content={
                "status": 999,
                "seat_name": selected_seat,
                "message": "seat hold success.",
            },
            status_code=200,
        )

    except Exception as e:
        error_detail = e.detail if hasattr(e, "detail") else str(e)

        return JSONResponse(
            content={"error": error_detail, "status": 999}, status_code=400
        )


def seat_hold_details_function(authenticate, details, db):
    seat_hold_model = (
        db.query(models.seat_hold_model)
        .filter(models.seat_hold_model.show_id == details.show_id)
        .all()
    )
    show_model = (
        db.query(models.show_model)
        .filter(models.show_model.show_id == details.show_id)
        .first()
    )
    seat_hold_data = []

    if not seat_hold_model:
        raise HTTPException(status_code=400, detail="Show not found.")

    for i in seat_hold_model:
        if authenticate["api_username"] == i.api_username:
            print("details.transaction_id", details.transaction_id)
            print("i.transaction_id", i.transaction_id)
            if details.transaction_id == i.transaction_id:
                single_seat_hold_data = {
                    "seat_name": i.seat_name,
                    "show_id": i.show_id,
                    "exipry_time": str(i.exipry_time),
                    "ticket_price": show_model.ticket_price,
                }
                seat_hold_data.append(single_seat_hold_data)

        else:
            raise HTTPException(
                status_code=400, detail="Invalid api_usernme. Check token."
            )
    print("seat_hold_data", seat_hold_data)
    return seat_hold_data


class seat_hold_detail_schema(BaseModel):
    show_id: int
    transaction_id: str


@seat_hold_router.post("/seat_hold_details")
def seat_hold_details(
    details: seat_hold_detail_schema,
    db: session = Depends(get_db),
    authenticate=Depends(auth.thirdparty_auth),
):
    try:
        a = seat_hold_details_function(authenticate, details, db)

        return JSONResponse(content={"data": a, "status": 999}, status_code=200)

    except Exception as e:
        error_detail = e.detail if hasattr(e, "detail") else str(e)

        return JSONResponse(
            content={"error": error_detail, "status": 999}, status_code=400
        )
