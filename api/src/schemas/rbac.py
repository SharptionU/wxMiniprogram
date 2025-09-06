from datetime import datetime

from pydantic import BaseModel


class WebLoginReqUser(BaseModel):
    username: str
    password: str


class WebLoginResUser(BaseModel):
    username: str
    id: str | None
    avatar: str | None
    jwt_token: str | None


class WebRegisterReqUser(BaseModel):
    username: str
    password: str


class WebRegisterResUser(BaseModel):
    username: str
    id: str | None
    message: str | None


class WXLoginReqUser(BaseModel):
    username: str
    password: str


class WXLoginResUser(BaseModel):
    username: str
    user_id: str | None
    jwt_token: str | None
    token_expires: datetime | None
