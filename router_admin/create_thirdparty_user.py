from fastapi import FastAPI, Depends, APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from router_admin.auth import auth_class
from sqlalchemy.orm import Session
from router_admin.base import get_db
import random
import string

from thirdparty.thirdparty_models import thirdparty_models


create_thirdparty_user_router = APIRouter()

auth = auth_class


class create_thirdparty_token_schema(BaseModel):
    api_username: str


def generate_random_alphanumeric(length):
    alphanumeric_chars = string.ascii_letters + string.digits
    return "".join(random.choices(alphanumeric_chars, k=length))


@create_thirdparty_user_router.post("/create_thirdparty_user")
def create_thirdparty_user(
    details: create_thirdparty_token_schema, db: Session = Depends(get_db)
):
    thirdparty_user_model = thirdparty_models.thirdparty_user_model()

    thirdparty_user_model.api_username = details.api_username
    thirdparty_user_model.api_password = generate_random_alphanumeric(8)
    thirdparty_user_model.api_secret = generate_random_alphanumeric(10)

    try:
        db.add(thirdparty_user_model)
        db.commit()

        theatre_auth_data_json = {
            "api_username": thirdparty_user_model.api_username,
            "api_password": thirdparty_user_model.api_password,
            "api_secret": thirdparty_user_model.api_secret,
        }

        return JSONResponse(
            content={
                "status": 000,
                "message": "Successfully added theatre data.",
                "data": theatre_auth_data_json,
            },
            status_code=200,
        )

    except Exception as e:
        return {"error": str(e)}
