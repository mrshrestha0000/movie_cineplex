from fastapi import Depends, APIRouter
from pydantic import BaseModel
from .base import get_db
from .auth import auth_class
from sqlalchemy.orm import session
import models
from fastapi.responses import JSONResponse




movie_router = APIRouter()
auth = auth_class()


class movie_info_schema(BaseModel):
    movie_name: str
    movie_type: str
    duration: int
    image: str



@movie_router.post('/movie_info')
def theatre_audi(
        details:movie_info_schema, 
        db:session = Depends(get_db), 
        authenticate = Depends(auth.mid)
        ):

    movie_model = models.movie_model()

    movie_model.theatre_id = authenticate['theatre_id']
    movie_model.movie_name = details.movie_name
    movie_model.movie_type = details.movie_type
    movie_model.duration = details.duration
    movie_model.image = details.image

    db.add(movie_model)
    db.commit()

    db.refresh(movie_model)

    movie_info_json = {
        "theatre_id":authenticate['theatre_id'],
        "movie_id":movie_model.movie_id,
        "movie_name":details.movie_name,
        "movie_type":details.movie_type,
        "duration":details.duration,
        "image":details.image
    }

    theatre_id = authenticate['theatre_id']
    return JSONResponse(content={
        "status":999,
        "audi_data":movie_info_json
    }, status_code=200)

    