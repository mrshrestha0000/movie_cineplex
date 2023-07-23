from fastapi import FastAPI, APIRouter, Request, HTTPException, Response
import models
from sqlalchemy.orm import Session
from database import SessionLocal
from datetime import datetime, timedelta
import jwt
from thirdparty.thirdparty_models import thirdparty_models
from fastapi.responses import JSONResponse

auth_router = APIRouter()
app = FastAPI()

SECRET_KEY = "1111"
ALGORITHM = "HS256"


class auth_class():


    # create access token
    def create_access_token(self, data:dict):
        expire = datetime.utcnow() + timedelta(minutes=100)
        data.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        encoded_jwt_json_data = {
            "token":encoded_jwt,
            "expire":expire
        }
        return encoded_jwt_json_data

    # create refresh token
    def create_refresh_token(self, data: dict):
        expire = datetime.utcnow() + timedelta(minutes=3600)
        data.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


    # decode tokens
    def decode_token(self, token):
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload


    # create middleware to authenticate
    def mid(self, request:Request):
        db = SessionLocal()
        try: 
            token_token = request.headers.get('Authorization')
            a = token_token.split(" ")[0]
            
            if a == "Token":
                token = token_token.split(" ")[1]
                user = db.query(models.theatre_auth_model).all()

            
                decode_auth = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
                type = decode_auth['type']
                api_username = decode_auth['api_username']
                api_password = decode_auth['api_password']
                api_secret = decode_auth['api_secret']
                theatre_id = decode_auth['theatre_id']

                for i in user:
                    if theatre_id == i.theatre_id and api_secret == i.api_secret and api_password == i.api_password and api_username == i.api_username:
                        return {"theatre_id":theatre_id, "type":"access"}


            if a != "Token":
                raise HTTPException (status_code=401, detail="Invalid Auth Prefix.")

            # except Exception as e: 
            #     raise HTTPException (status_code=401, detail="Invalid Auth. Exception error")
            
            if type == "refresh":
                raise HTTPException (status_code=401, detail="Invalid Auth. You are using refresh token.")

        except Exception as e:
            raise HTTPException (status_code=401, detail= str(e))

        db.close()
        
        




    def thirdparty_auth(self, request:Request):
        db = SessionLocal()
        try: 
            
            
            token_token = request.headers.get('Authorization')

            if token_token is None:
                raise HTTPException (status_code=401, detail="Auth Not provided")

            a = token_token.split(" ")[0]

            if a == "Token":
                token = token_token.split(" ")[1]
                user = db.query(thirdparty_models.thirdparty_user_model).all()

            
                decode_auth = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
                type = decode_auth['type']
                api_username = decode_auth['api_username']
                api_password = decode_auth['api_password']
                api_secret = decode_auth['api_secret']
                

                for i in user:
                    if api_username == i.api_username and api_secret == i.api_secret and api_password == i.api_password:
                        return {"api_username":api_username, "type":"access"}


            if a != "Token":
                raise HTTPException (status_code=401, detail="Invalid Auth Prefix.")

            # except Exception as e: 
            #     raise HTTPException (status_code=401, detail="Invalid Auth. Exception error")
            
            if type == "refresh":
                raise HTTPException (status_code=401, detail="Invalid Auth. You are using refresh token.")

        except Exception as e:
            raise HTTPException (status_code=401, detail= str(e))

        db.close()
    


