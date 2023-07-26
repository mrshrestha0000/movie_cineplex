from fastapi import FastAPI, Depends, APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from router_admin.auth import auth_router
from router_admin.create_token import token_router
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models
from router_admin.base import get_db
import random, string


add_theatre_and_create_auth_data_router = APIRouter()


def generate_random_alphanumeric(length):
    alphanumeric_chars = string.ascii_letters + string.digits
    return "".join(random.choices(alphanumeric_chars, k=length))


def theatre_auth_data_save(id: int, db):
    theatre_auth_model = models.theatre_auth_model()

    theatre_auth_model.theatre_id = id
    theatre_auth_model.api_username = generate_random_alphanumeric(7)
    theatre_auth_model.api_password = generate_random_alphanumeric(8)
    theatre_auth_model.api_secret = generate_random_alphanumeric(10)

    try:
        db.add(theatre_auth_model)
        db.commit()

        theatre_auth_data_json = {
            "theatre_id": theatre_auth_model.theatre_id,
            "api_username": theatre_auth_model.api_username,
            "api_password": theatre_auth_model.api_password,
            "api_secret": theatre_auth_model.api_secret,
        }

        return theatre_auth_data_json

    except Exception as e:
        return {"error": str(e)}


class theatre__info_schema(BaseModel):
    theatre_code: str
    theatre_name: str
    location_id: int
    location_name: str
    address: str
    vat_number: str
    contact: str


@add_theatre_and_create_auth_data_router.post("/add_theatre_info/")
def create_user(
    thretre_info_instance: theatre__info_schema, db: Session = Depends(get_db)
):
    try:
        theatre_info = models.theatre_info_model()

        theatre_info.theatre_code = thretre_info_instance.theatre_code
        theatre_info.theatre_name = thretre_info_instance.theatre_name
        theatre_info.location_id = thretre_info_instance.location_id
        theatre_info.location_name = thretre_info_instance.location_name
        theatre_info.address = thretre_info_instance.address
        theatre_info.vat_number = thretre_info_instance.vat_number
        theatre_info.contact = thretre_info_instance.contact

        try:
            db.add(theatre_info)
            db.commit()

            db.refresh(theatre_info)
            theatre_id = theatre_info.theatre_id

            get_token_info = theatre_auth_data_save(theatre_id, db)

            theatre_info_json = {
                "theatre_id": theatre_id,
                "theatre_code": theatre_info.theatre_code,
                "theatre_name": theatre_info.theatre_name,
                "location_id": theatre_info.location_id,
                "location_name": theatre_info.location_name,
                "address": theatre_info.address,
                "vat_number": theatre_info.vat_number,
                "contact": theatre_info.contact,
                "get_token_info": get_token_info,
            }

            return JSONResponse(
                content={
                    "status": 000,
                    "message": "Successfully added theatre data.",
                    "data": theatre_info_json,
                },
                status_code=200,
            )

        except Exception as e:
            return JSONResponse(
                content={
                    "error": "Could not save theatre.",
                    "status": 999,
                    "detail": str(e),
                },
                status_code=400,
            )

    except Exception as e:
        return JSONResponse(
            content={
                "error": "Could not create theatre.",
                "status": 999,
                "detail": str(e),
            },
            status_code=400,
        )
