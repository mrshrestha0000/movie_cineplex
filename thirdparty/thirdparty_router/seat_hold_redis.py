from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from router_admin.base import get_db
from router_admin.auth import auth_class
from sqlalchemy.orm import session
import models
import redis, json
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from thirdparty.thirdparty_models import thirdparty_models
from thirdparty.thirdparty_router.get_seat import seat_list

seat_hold_router = APIRouter()
auth = auth_class()
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)


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


# constructor_for_seat_list = {
#     "theatre_id": show_model.theatre_id,
#     "audi_id": show_model.audi_id,
#     "movie_id": show_model.movie_id,
#     "show_id": show_model.show_id,
#     "transaction_id": details.transaction_id,
# }


# seat_available = validate_seat_avaibility(
#     constructor_for_seat_list, seat_name, db, authenticate
# )
def validate_seat_avaibility_redis(details, seat_name: list, db, authenticate):
    for i in range(len(seat_name)):
        list_of_seat = seat_list(details, db)
        # print("list_of_seat", list_of_seat)

        keys = redis_client.scan_iter(match="*", count=100)
        all_data = {}
        seat_hold_model = []
        for key in keys:
            value = redis_client.get(key)
            if isinstance(value, bytes):
                value = value.decode("utf-8")

            try:
                json_data = json.loads(value)
                all_data[key.decode("utf-8")] = json_data

                for key, value in all_data.items():
                    if value.get("api_username") is None:
                        continue
                    if authenticate["api_username"] == value["api_username"]:
                        seat_hold_model.append(value)

            except json.JSONDecodeError:
                all_data[key.decode("utf-8")] = value

        # seat_hold_model = (
        #     db.query(models.seat_hold_model)
        #     .filter(models.seat_hold_model.transaction_id == details["transaction_id"])
        #     .all()
        # )

        # seat_hold_model_redis = {}

        for k in seat_hold_model:
            print("seat_hold_model", k)
            if k["transaction_id"] == details["transaction_id"]:
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

                # db.add(seat_hold_model)
                # db.commit()

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


@seat_hold_router.post("/seat_hold_redis")
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
        redis_key_data = []

        # if show_model is None:
        #     return JSONResponse(
        #         content={"status": 999, "error": "Invalid show id."}, status_code=400
        #     )

        constructor_for_seat_list = {
            "theatre_id": show_model.theatre_id,
            "audi_id": show_model.audi_id,
            "movie_id": show_model.movie_id,
            "show_id": show_model.show_id,
            "transaction_id": details.transaction_id,
        }

        seat_available = validate_seat_avaibility_redis(
            constructor_for_seat_list, seat_name, db, authenticate
        )

        print("seat_available", seat_available)

        for i in range(len(seat_name)):
            seat_detail_model = (
                db.query(models.seat_detail_model)
                .filter(models.seat_detail_model.seat_name == seat_name[i])
                .first()
            )
            # show_model = (
            #     db.query(models.show_model)
            #     .filter(models.show_model.show_id == show_id)
            #     .first()
            # )
            # seat_hold_model = models.seat_hold_model()

            # if seat_detail_model is None:
            #     return JSONResponse(
            #         content={"error": "Inavlid seat name", "status": 999},
            #         status_code=400,
            #     )

            if seat_detail_model is not None:
                current_datetime = datetime.now()
                seat_hold_expire_datetime = current_datetime + timedelta(minutes=10)

                print("seat_name", seat_name[i])
                redis_key = f"{seat_name[i]}"

                # seat_hold_model.show_id = show_id
                # seat_hold_model.seat_name = seat_name[i]
                # seat_hold_model.exipry_time = seat_hold_expire_datetime
                # seat_hold_model.transaction_id = transaction_id
                # seat_hold_model.api_username = authenticate["api_username"]

                # print("authenticate", authenticate["api_username"])

                seat_hold_json = {
                    "seat_name": seat_name[i],
                    "show_id": show_id,
                    "seat_hold_expire_datetime": str(seat_hold_expire_datetime),
                    "transaction_id": transaction_id,
                    "api_username": authenticate["api_username"],
                    "amount":show_model.ticket_price
                }
                redis_client.setex(redis_key, 600, json.dumps(seat_hold_json))

                selected_seat.append(seat_name[i])
                redis_key_data.append(redis_key)

            # print("selected_seat", selected_seat)
            # print("redis_key_data", redis_key_data)

        return JSONResponse(
            content={
                "status": 999,
                "seat_name": "selected_seat",
                "message": "seat hold success.",
            },
            status_code=200,
        )

    except Exception as e:
        error_detail = e.detail if hasattr(e, "detail") else str(e)

        return JSONResponse(
            content={"error": error_detail, "status": 999}, status_code=400
        )


#  seat_hold_details_function(authenticate, details, db)
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
    return seat_hold_data


def seat_hold_details_function_redis(authenticate, details, db):
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
            # print("details.transaction_id", details.transaction_id)
            # print("i.transaction_id", i.transaction_id)
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
    # print("seat_hold_data", seat_hold_data)
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


def seat_hold_data_by_txnid_seatname_apiusername(txnid, apiusername):
    
    keys = redis_client.scan_iter(match="*", count=100) 

    all_data = {}
    filtered_data = {}

    for key in keys:
        value = redis_client.get(key)

        if isinstance(value, bytes):
            value = value.decode("utf-8")

        try:
            json_data = json.loads(value)
            all_data[key.decode("utf-8")] = json_data
            for key, value in all_data.items():
                if value["transaction_id"] == txnid and value["api_username"] == apiusername:
                    filtered_data[key] = value 

        except json.JSONDecodeError:
            all_data[key.decode("utf-8")] = value
    return (filtered_data)


@seat_hold_router.post("/seat_hold_details_redis")
def seat_hold_details_redis(
    details: seat_hold_detail_schema,
    db: session = Depends(get_db),
    authenticate=Depends(auth.thirdparty_auth),
):  
        
    
    filtered_data = seat_hold_data_by_txnid_seatname_apiusername(txnid=details.transaction_id, apiusername=authenticate['api_username'])

    return filtered_data


# @seat_hold_router.post("/get_data_by_show_id_and_txn_id")
# def get_data_by_show_id_and_txn_id( details: seat_hold_detail_schema,
#     db: session = Depends(get_db),
#     authenticate=Depends(auth.thirdparty_auth),):


def seat_hold_release_redis(seat_name):
    keys = redis_client.scan_iter(match="*", count=100)
    all_data = {}
    for key in keys:
        print ("key", key)
        print ("seat_name", seat_name)
        if key == seat_name:
            redis_client.delete(key)

    return True
        # else:
        #     raise HTTPException(
        #         status_code=400, detail="Seat cannot be removed from seat hold."
        #     )
