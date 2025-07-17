import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import auth, tasks
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from app.db.database import create_database_if_not_exists, async_engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 起動前処理
    await create_database_if_not_exists()
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Lifespan startup 完了")
    yield

# FastAPIのインスタンス
app = FastAPI(lifespan=lifespan)
# routers内で定義したrouterのインスタンスをFastAPIをインストール
app.include_router(tasks.router)
app.include_router(auth.router)

# CORSの設定
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 確認用のエンドポイント
@app.get("/api/hello")
async def hello():
    return {"message": "hello world!"}