from fastapi import FastAPI
from database.main import Database
from server.dataModels.models import User
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
print('start')

path = 'localhost'
if 'MY_PATH' in os.environ:
    path = os.environ["MY_PATH"]

database = Database()


@app.post("/auth/registration")
def registration(user: User) -> object:
    results = database.put_user(user.login, user.password, user.email)
    response = {
        "resultCode": 0,
        "email": user.email,
        "login": user.login
    }
    if results[0] == "0":
        return response
    else:
        response["resultCode"] = 1
        response["email"] = ""
        response["login"] = ""
        return response


@app.post("/auth/login")
def login(user: User) -> object:
    results = database.take_user(user.login)

    response = {
        "resultCode": 1,
        "email": "",
        "login": ""
    }

    if results[0] == "1":
        return response
    elif results[0][2] == user.password:
        response = {
            "resultCode": 0,
            "email": results[0][3],
            "login": results[0][1]
        }
        return response
    else:
        response["resultCode"] = 2
        return response



origins = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
