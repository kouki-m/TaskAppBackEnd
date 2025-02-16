from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
import uuid

import app.cruds.auth as auth_crud
from app.db.database import get_db
import app.schemas.auth as auth_schema


router = APIRouter()


# ユーザー登録API
@router.post("/api/auth/signup", response_model=auth_schema.UserRegisterResponse)
async def register_user(
    user_information: auth_schema.UserRegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    return await auth_crud.register_user(db, user_information)


# ユーザー認証API
@router.post("/api/auth/login", response_model=auth_schema.UserLoginResponse)
async def login_user(
    user_information: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await auth_crud.login_user(db, user_information)


# ユーザー認証　テスト
from app.models.tasks import User
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: uuid.UUID
    employee_id: int
    username: str


@router.get("/api/auth/test", response_model=UserResponse)
async def test_user(user: User = Depends(auth_crud.varify_token)):
    return UserResponse(
        id=user.id, employee_id=user.employee_id, username=user.username
    )
