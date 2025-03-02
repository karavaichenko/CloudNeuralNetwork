from pydantic import BaseModel


class User(BaseModel):
    login: str
    password: str
    email: str = None
