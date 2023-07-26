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


thirdparty_token_router = APIRouter()

auth = auth_class()


class thirdparty_token_schema(BaseModel):
    api_username: str
    api_password: str
    api_secret: str


@thirdparty_token_router.post("/auth")
def create_thirdparty_token(
    details: thirdparty_token_schema, db: Session = Depends(get_db)
):
    try:
        thirdparty_user_model = (
            db.query(thirdparty_models.thirdparty_user_model)
            .filter(
                thirdparty_models.thirdparty_user_model.api_username
                == details.api_username
            )
            .first()
        )

        if thirdparty_user_model is None:
            return JSONResponse(
                content={"error": "Invlalid auth", "status": 999}, status_code=400
            )

        if (
            details.api_username == thirdparty_user_model.api_username
            and details.api_password == thirdparty_user_model.api_password
            and details.api_secret == thirdparty_user_model.api_secret
        ):
            api_username = details.api_username
            api_password = details.api_password
            api_secret = details.api_secret

            thirdparty_auth_json_data = {
                "api_username": api_username,
                "api_password": api_password,
                "api_secret": api_secret,
            }

            auth_data = auth.create_access_token(thirdparty_auth_json_data)

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
