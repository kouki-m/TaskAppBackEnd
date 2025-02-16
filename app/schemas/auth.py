from pydantic import Field
import uuid

from app.schemas.base_schema import BaseSchema


class UserRegisterRequest(BaseSchema):
    email: str = Field(..., example="example@example.com")
    password: str = Field(..., example="password001")


class UserRegisterResponse(BaseSchema):
    message: str = Field(..., example="User registered successfully")
    access_token: str


class UserLoginResponse(BaseSchema):
    access_token: str
    token_type: str
