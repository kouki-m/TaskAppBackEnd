# python3.12のイメージをダウンロード
FROM python:3.12-bullseye
ENV PYTHONUNBUFFERED=1

WORKDIR /src

# pipを使ってpoetryをインストール
RUN pip install poetry==1.8.4

# アプリケーションをコピー
COPY . ./

# poetryでライブラリをインストール
RUN if [ -f pyproject.toml ]; then echo "pyproject.tomlが見つかりました。poetry installを実行します。"; poetry install --no-root; else echo "pyproject.tomlが見つかりませんでした。"; fi

# uvicornのサーバーを立ち上げる
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]