# This file is responsible for signing, encoding, decoding and returning JWTs

import time

import jwt
from decouple import config


JWT_SECRET = config("secret")
JST_ALGORITHM = config("algorithm")


# Functioin returns the generated Tokens (JWTs)
def token_response(token: str):
    return {
        "access_token": token
    }


# Function user for signing the JWT string
def signJWT(userID: str):
    payload = {
        "userID": userID,
        "expiry": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JST_ALGORITHM)
    return token_response(token)

def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JST_ALGORITHM)
        return decode_token if decode_token['expires'] >= time.time() else None
    except:
        return {}