import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# .envファイルを読み込む
load_dotenv()

# DB URLに必要な情報を環境変数から取得
db_user = os.getenv("MYSQL_USER")  # データベースのユーザー名
db_host = os.getenv("MYSQL_HOST")  # データベースのホスト名
db_passwd = os.getenv("MYSQL_ROOT_PASSWORD")  # データベースのパスワード
db_name = os.getenv("MYSQL_DB_NAME")  # データベースの名前

# 非同期用のデータベース接続URLを構築
ASYNC_DB_URL = (
    f"mysql+aiomysql://{db_user}:{db_passwd}@{db_host}/{db_name}?charset=utf8"
)


# 非同期エンジンの作成
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
# 非同期セッションの作成
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)


# データベースの基本クラスを定義
Base = (
    declarative_base()
)  # SQLAlchemyのマッピングで使用する基本クラス。これを継承して各モデル（テーブル）を定義する。


# 非同期でデータベースセッションを取得する関数
async def get_db():
    async with async_session() as session:
        yield session
