#here i encode and decode password using base64
from fastapi import FastAPI
from pydantic import BaseModel
import base64




# Encode password using Base64
def encode_password(password):
    encoded_bytes = base64.b64encode(password.encode("utf-8"))
    a = encoded_bytes.decode("utf-8")
    return a
    

# Decode password using Base64
def decode_password(encoded_password):
    decoded_bytes = base64.b64decode(encoded_password.encode("utf-8"))
    a = decoded_bytes.decode("utf-8")
    return a
   

a = encode_password("samip")
b = str(a)
c = type(a)
print(a)
print (c)
decode = decode_password(a)
print("decode",decode)