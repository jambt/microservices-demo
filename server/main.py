import asyncio
import requests
import json
import functools

from fastapi import FastAPI, Form
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")


async def post_request(url: str, password: str):
    loop = asyncio.get_event_loop()
    known_passwords = loop.run_in_executor(
        None,
        functools.partial(
            requests.post,
            url,
            json={
                "password": password
            }
        )
    )
    return await known_passwords


@app.get("/")
async def index():
    return templates.TemplateResponse("index.html", {"request": {}})


@app.post("/password")
async def check_password(password: str=Form(...)):

    checker_response = await post_request('http://password-checker/check-password', password)
    dedup_response = await post_request('http://password-dedup/check-password', password)
    known_response = await post_request('http://known-passwords/check-password', password)

    return templates.TemplateResponse(
        "password.html",
        {
            "request": {},
            "quality": json.loads(checker_response.text),
            "dedup": json.loads(dedup_response.text),
            "known": json.loads(known_response.text)
        }
    )
