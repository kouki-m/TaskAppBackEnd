import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import auth, tasks
from dotenv import load_dotenv


# FastAPIのインスタンス
app = FastAPI()
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
@app.get("/hello")
async def hello():
    return {"message": "hello world!"}
