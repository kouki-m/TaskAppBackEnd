from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
import os
from dotenv import load_dotenv
from app.models.tasks import User
import app.schemas.auth as auth_schema
from app.db.database import get_db

# パスワードのハッシュ化用設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
load_dotenv(dotenv_path="/src/.env")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30


### ユーザー登録関連
async def get_user_by_email(db: AsyncSession, email: str):
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def register_user(
    db: AsyncSession, user_information: auth_schema.UserRegisterRequest
):
    existing_user = await get_user_by_email(db, user_information.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail already registered",
        )

    hashed_password = get_password_hash(user_information.password)
    new_user = User(
        email=user_information.email,
        password=hashed_password,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(new_user)
    access_token = create_access_token(
        data={"sub": new_user.email},
        expires_delta=timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS),
    )
    await db.commit()
    await db.refresh(new_user)
    return auth_schema.UserRegisterResponse(
        message="User registered successfully", access_token=access_token
    )


### ログイン関連


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def login_user(db: AsyncSession, user_information: OAuth2PasswordRequestForm):
    user = await authenticate_user(
        db, user_information.username, user_information.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return auth_schema.UserLoginResponse(access_token=access_token, token_type="bearer")


### トークン検証
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def varify_token(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            print("employee_id is None")
            raise credentials_exception
    except JWTError:
        print("JWTError")
        raise credentials_exception
    user = await get_user_by_email(db, email)
    if user is None:
        print("user is None")
        raise credentials_exception
    return user
