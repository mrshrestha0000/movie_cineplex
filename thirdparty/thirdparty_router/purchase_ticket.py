from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from router_admin.base import get_db
from router_admin.auth import auth_class
from sqlalchemy.orm import session
import models, copy
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta

from thirdparty.thirdparty_router.seat_hold import seat_hold_details_function
from router_admin.create_thirdparty_user import generate_random_alphanumeric
from sqlalchemy import and_
from thirdparty.thirdparty_router.seat_hold import seat_hold_details_function

purchase_ticket_router = APIRouter()
auth = auth_class()


def purchase_ticket_validation(details, db):
    purchase_ticket_model = (
        db.query(models.purchase_ticket_model)
        .filter(models.purchase_ticket_model.show_id == details["show_id"])
        .all()
    )
    purchase_ticket_model_filter_by_api_username = (
        db.query(models.purchase_ticket_model)
        .filter(models.purchase_ticket_model.api_username == details["api_username"])
        .all()
    )
    for i in purchase_ticket_model:
        print(details["seat_name"])
        print(i.seat_name)
        if details["seat_name"] == i.seat_name:
            raise HTTPException(status_code=400, detail="Seat already purchased.")
        for j in purchase_ticket_model_filter_by_api_username:
            print(details["transaction_id"])
            print(j.transaction_id)
            if str(details["transaction_id"]) == str(j.transaction_id):
                raise HTTPException(status_code=400, detail="Duplicate transaction_id")

    return True


def seat_remove_from_seat_hold(details, db):
    seat_hold_model = (
        db.query(models.seat_hold_model)
        .filter(
            and_(
                models.seat_hold_model.show_id == details["show_id"],
                models.seat_hold_model.seat_name == details["seat_name"],
            )
        )
        .first()
    )

    if seat_hold_model:
        print("seat_hold_model", seat_hold_model.__dict__)
        db.delete(seat_hold_model)
        db.commit()
        return True

    else:
        raise HTTPException(status_code=400, detail="Seat not found in seat hold data.")


class purchase_ticket_schema(BaseModel):
    show_id: int

    transaction_id: str
    amount: float


@purchase_ticket_router.post("/purchase_ticket")
def purchase_ticket(
    details: purchase_ticket_schema,
    db: session = Depends(get_db),
    authenticate=Depends(auth.thirdparty_auth),
):
    try:
        seat_hold_data = seat_hold_details_function(authenticate, details, db)
        purchase_ticket_model = models.purchase_ticket_model()
        show_model = (
            db.query(models.show_model)
            .filter(models.show_model.show_id == details.show_id)
            .first()
        )
        theatre_id = show_model.theatre_id
        theatre_info_model = (
            db.query(models.theatre_info_model)
            .filter(models.theatre_info_model.theatre_id == theatre_id)
            .first()
        )
        show_model = (
            db.query(models.show_model)
            .filter(models.show_model.show_id == details.show_id)
            .first()
        )
        audi_id = show_model.audi_id
        theatre_audi_model = (
            db.query(models.theatre_audi_model)
            .filter(models.theatre_audi_model.audi_id == audi_id)
            .first()
        )
        movie_model = (
            db.query(models.movie_model)
            .filter(models.movie_model.movie_id == show_model.movie_id)
            .first()
        )

        amount = 0
        for i in seat_hold_data:
            amount = i["ticket_price"] + amount

        print("seat_hold_data", seat_hold_data)

        if details.amount == amount:
            ticket_detail = []
            purchase_ticket_models = []

            for j in seat_hold_data:
                validate_ticket_purhase_json = {
                    "show_id": details.show_id,
                    "seat_name": j["seat_name"],
                    "transaction_id": details.transaction_id,
                    "api_username": authenticate["api_username"],
                }

                print("validate_ticket_purhase_json", validate_ticket_purhase_json)

                validate_ticket_purhase_model = purchase_ticket_validation(
                    validate_ticket_purhase_json, db
                )

                purchase_ticket_model.amount = j["ticket_price"]
                purchase_ticket_model.transaction_id = details.transaction_id
                purchase_ticket_model.seat_name = j["seat_name"]
                purchase_ticket_model.api_username = authenticate["api_username"]
                purchase_ticket_model.audi_id = show_model.audi_id
                purchase_ticket_model.show_id = j["show_id"]
                a = j["seat_name"]

                purchase_ticket_models.append(copy.deepcopy(purchase_ticket_model))

            print("purchase_ticket_models, ", purchase_ticket_models)

            db.add_all(purchase_ticket_models)
            db.commit()

            for l in purchase_ticket_models:
                db.refresh(l)

                param_cons_for_seat_hold_rm = {
                    "seat_name": l.seat_name,
                    "show_id": l.show_id,
                    "transaction_id": l.transaction_id,
                }
                print("param_cons_for_seat_hold_rm", param_cons_for_seat_hold_rm)
                seat_remove_from_seat_hold(param_cons_for_seat_hold_rm, db)

            new_purchase_ticket_model = (
                db.query(models.purchase_ticket_model)
                .filter(
                    models.purchase_ticket_model.transaction_id
                    == details.transaction_id
                )
                .all()
            )
            for i in new_purchase_ticket_model:
                single_ticket_details = {
                    "ticket_id": i.ticket_id,
                    "theatre_name": theatre_info_model.theatre_name,
                    "location_name": theatre_info_model.location_name,
                    "audi_name": theatre_audi_model.audi_name,
                    "movie_name": movie_model.movie_name,
                    "movie_type": movie_model.movie_type,
                    "duration": movie_model.duration,
                    "show_date": str(show_model.startTime),
                    "ticket_price": show_model.ticket_price,
                    "seat_name": i.seat_name,
                }

                ticket_detail.append(single_ticket_details)

            return JSONResponse(
                content={
                    "transaction_id": details.transaction_id,
                    "status": 000,
                    "message": "Ticket_purchase_successful.",
                    "tickets": ticket_detail,
                },
                status_code=200,
            )
        else:
            return JSONResponse(content={"message": "amount mismatch.", "status": 999})

    except Exception as e:
        import traceback

        traceback.print_exc()

        error_detail = e.detail if hasattr(e, "detail") else str(e)
        return JSONResponse(
            content={"error": error_detail, "status": 999}, status_code=400
        )
