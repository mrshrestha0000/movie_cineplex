from fastapi import Depends, APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from database import engine
from sqlalchemy.orm import Session
import models
import database
from .auth import auth_class
from .base import get_db


token_router = APIRouter()

auth = auth_class()

database.Base.metadata.create_all(bind=engine)


class generate_token_schema(BaseModel):
    theatre_id: int
    api_username: str
    api_password: str
    api_secret: str


@token_router.post("/token/")
def generate_token(detail: generate_token_schema, db: Session = Depends(get_db)):
    try:
        theatre_auth_model = (
            db.query(models.theatre_auth_model)
            .filter(models.theatre_auth_model.theatre_id == detail.theatre_id)
            .first()
        )

        if theatre_auth_model is None:
            return JSONResponse(
                content={"error": "Invlalid Theatre", "status": 999}, status_code=400
            )

        if (
            detail.api_username == theatre_auth_model.api_username
            and detail.api_password == theatre_auth_model.api_password
            and detail.api_secret == theatre_auth_model.api_secret
        ):
            api_username = detail.api_username
            api_password = detail.api_password
            api_secret = detail.api_secret
            theatre_id = detail.theatre_id

            theatre_auth_json_data = {
                "api_username": api_username,
                "api_password": api_password,
                "api_secret": api_secret,
                "theatre_id": theatre_id,
            }

            auth_data = auth.create_access_token(theatre_auth_json_data)

            token = auth_data["token"]
            expire = str(auth_data["expire"])

            return JSONResponse(
                content={"token": token, "expire": expire, "status": 000},
                status_code=200,
            )

        else:
            return JSONResponse(
                content={"error": "Invlalid credentials.", "status": 999},
                status_code=400,
            )

    except Exception as e:
        return JSONResponse(content={"error": str(e), "status": 999}, status_code=400)
