from fastapi import FastAPI , Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
# from .router.auth import auth_router
from router.auth import auth_router
from database import SessionLocal, engine
from sqlalchemy.orm import Session
# from models import theatre_info_model
import models
import database


app = FastAPI()
app.include_router(auth_router, prefix='/auth')

database.Base.metadata.create_all(bind=engine)
# database.Base.metadata.create_all(bind = database.engine)


async def get_db():
    try: 
        db = SessionLocal()
        yield db 
    finally:
        db.close()



class generate_token(BaseModel):
    api_username : str 
    api_password : str
    api_secret : str
    
@app.post("/generate_token/")
def generate_token(detail:generate_token):
    print (detail.api_secret)
    return JSONResponse (content={
        "a":"c"
    }, status_code=200)


class theatre_instance(BaseModel):
    theatre_id  : int
    theatre_code: str
    theatre_name: str
    location_id: int
    location_name: str
    address: str
    vat_number: str
    contact: str

@app.post('/add_theatre_info/')
def create_user(thretre_info_instance : theatre_instance, db: Session = Depends(get_db)):
    try: 
        theatre_info = models.theatre_info_model()

        #parsing data 
        theatre_info.theatre_id = thretre_info_instance.theatre_id
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

            theatre_info_json = {
                "theatre_code":theatre_info.theatre_code,
                "theatre_name":theatre_info.theatre_name,
                "location_id":theatre_info.location_id,
                "location_name":theatre_info.location_name,
                "address":theatre_info.address,
                "vat_number":theatre_info.vat_number,
                "contact":theatre_info.contact
            }
            return JSONResponse(content={
                "status":000,
                "message":"Successfully added theatre data.",
                "data": theatre_info_json
            }, status_code=200)
        
        except Exception as e:
            return JSONResponse(content={
                "error":"Could not save theatre.",
                "status":999,
                "detail":str(e)
            },
            status_code=400) 
  
    except Exception as e:
        return JSONResponse(content={
            "error":"Could not create theatre.",
            "status":999,
            "detail":str(e)
        },
         status_code=400) 







