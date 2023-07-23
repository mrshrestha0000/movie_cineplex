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

get_movie_router = APIRouter()
 
class theatre_movie(BaseModel):
    theatre_id : int

@get_movie_router.post('/get_movie')
def get_movie(details : theatre_movie, db: Session = Depends(get_db), authenticate =Depends(auth.thirdparty_auth)):
    # theatre_info_model = models.theatre_info_model.all()
    movie_model = db.query(models.movie_model).filter(models.movie_model.theatre_id == details.theatre_id)
    list_movie = []

    if movie_model is None:
        return JSONResponse(content={
            "status":999, 
            "message":f"Movie with {details['theatre_id']} not found"
        }, status_code=400)

    else:
        for i in movie_model:
            single_movie = {
                "movie_id":i.movie_id,
                "movie_name":i.movie_name,
                "movie_type":i.movie_type,
                "duration":i.duration,
                "image":i.image
            }

            list_movie.append(single_movie)

        return JSONResponse(content={
            "status":000,
            "data": list_movie
        }, status_code=200)

    

