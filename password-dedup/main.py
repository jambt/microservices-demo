import math
from fastapi import FastAPI
from pydantic import BaseModel
import redis


app = FastAPI()
redis_db = redis.Redis(host='redis', port=6379, db=0, charset="utf-8", decode_responses=True)
REDIS_PASSWORD_COLLECTION = 'old_passwords'


class Password(BaseModel):
    password: str


@app.post("/check-password")
async def check_password(password: Password):
    global redis_db

    pipe = redis_db.pipeline()
    pipe.lrange(REDIS_PASSWORD_COLLECTION, 0, 9)
    pipe.lpush(REDIS_PASSWORD_COLLECTION, password.password)
    pipe.ltrim(REDIS_PASSWORD_COLLECTION, 0, 9)
    ret = pipe.execute()

    old_passwords = ret[0]

    print(old_passwords)
    answer = password.password in old_passwords

    return answer
