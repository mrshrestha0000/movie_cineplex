from fastapi import APIRouter, Request, Response
import json

# from fastapi_redis_cache import FastApiRedisCache, cache
# from sqlalchemy.orm import Session

redis_router = APIRouter()

import redis

# r = redis.Redis(host="localhost", port=6379, decode_responses=True)
# r.set("foo", "bar")
# a = r.ping()
# print(a)


# redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)
# redis_client.set("my_key", "my_value")
# data = {"name": "John", "age": 30}
# data1 = {"name": "John", "age": 30}
# redis_client.setex("user_infos", 10, json.dumps(data1))
