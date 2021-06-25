import math
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Password(BaseModel):
    password: str


# Load known password list
KNOWN_PW = set()
with open('passwords.txt', 'r') as file:
    for pw in file.readlines():
        KNOWN_PW.add(pw[:-1])  # [:-1] removes newline character
for p in KNOWN_PW:
    print(p)
    break


@app.post("/check-password")
async def check_password(password: Password):
    global KNOWN_PW
    return password.password in KNOWN_PW
