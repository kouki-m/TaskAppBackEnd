# README.md テンプレート

## 開発環境

## ディレクトリ構成

<!-- Treeコマンドを使ってディレクトリ構成を記載 -->

```
.
├── app
│   ├── api　#FastAPIのエンドポイントの定義を行うディレクトリ
│   ├── cruds #DB操作（Create, Read, Update, Delete）を定義
│   ├── db #SQLAlchemyの設定、migrationファイルの保存
│   ├── models #SQLAlchemyのテーブル定義
│   ├── schemas #SQLAlchemyのリクエスト・レスポンスボディの型の定義
│   ├── service #APIで用いられる関数
│   ├── test #testコードやtestデータの保存
│   └── main.py
├── .env #アプリケーション全体で使用する環境変数を定義
├── .gitignore
├── Dockerfile
├── docker-compose.yaml
├── alembic.ini # alembicを実行するためのファイル
├── poetry.lock # Poetryによって生成された依存関係の固定ファイル
├── pyproject.toml # プロジェクトの依存関係を定義するファイル
└── README.md
```

## 開発環境設定

### ①env ファイルの作成


## 開発環境設定
### ①envファイルの作成
.env ファイルに、データベース接続情報とAPIのurlとkeyを含める。以下のような形式で記述


```
MYSQL_USER=root
MYSQL_HOST=db:3306
MYSQL_ROOT_PASSWORD=password #任意
MYSQL_DB_NAME=init_db # 初期データベースとしてdb_initを設定

SECRET_KEY=abcdefg1234567890

```
＊keyなどに=がある場合は、""で囲ってください

### ② コンテナの構築、起動

以下のコマンドで、開発環境を構築して起動

```
docker compose up --build
```

Docker イメージがビルドされ、FastAPI サーバーがバックグラウンドで起動
データベースの MySQL コンテナも同時に起動

アプリケーションが起動したら、ブラウザで http://localhost:8000/hello にアクセスして
{"message":"hello world"}が表示されるか確認

#### 開発環境を再構築する場合

##### コンテナの停止

コンテナ：アプリケーションの実行環境

＊Docker Compose で構築した場合、新しい構成を適用する際に既存のコンテナを削除するのが基本

```
docker compose down  # Composeで立ち上げたコンテナを一括停止・削除
```

もしくは、

```
docker ps -a  #すべてのコンテナを表示
docker rm <コンテナ名> -f  # コンテナを強制終了して削除
```

##### image の削除

image：アプリケーションのコードや依存関係、環境設定が含まれたもの

＊イメージの構成や Dockerfile に変更を加えた場合

```
docker image ls  #イメージを表示
docker rmi <イメージIDまたは名前>  # 個別のイメージを削除
```

##### volume の削除

volume：コンテナの永続データを保持するための領域

＊データを初期化したい場合や、不要なボリュームが増えてしまった場合、データベースの設定を一からやり直したい場合等

方法 ①（ボリュームを指定する方法）

```
docker volume ls  #ボリュームの表示
docker volume rm <ボリューム名>
```

方法 ②(使われていない volume すべて削除)

```
docker volume prune
```

##### キャシュを用いずに build

キャシュ：ビルドやデータの再利用を効率的に行うための一時的な保存領域

＊Dockerfile の内容を大きく変更した場合や、新しいライブラリを追加した場合には、キャッシュを無視してビルドすることで、変更が正しく反映される

```
docker compose build --no-cache

```

＊上記を実行する場合、コンテナは作成されないため、compose compose up を実行してください

```
docker compose up
```

### ③DB の初期設定

#### マイグレーションファイルの内容をデータベースに反映

- docker compose up でコンテナ起動後、 下記のログが出力された後下記のコマンドを実行してください

[Server] /usr/sbin/mysqld: ready for connections.

```
docker compose exec app poetry run alembic upgrade head
```

## 開発

app/ ディレクトリ内でファイルを編集すると、変更はコンテナ内で自動的に反映されます。

### コンソールの起動

Docker コンテナの中にシェルとして入る場合は、以下のコマンドを使用します。

```
docker compose exec app sh
```

### パッケージのインストール

#### ①lock ファイルと toml ファイルを作成

コンテナ内で新しいパッケージをインストールする場合は、以下のように poetry コマンドを使用します。

```
docker compose exec app poetry add <パッケージ名>
```

変更内容は、poetry.lock poetry.toml に反映される

#### ② 環境に適用

```
docker compose build --no-cache

```

### データベース関係

#### データベースに変更を加える場合

##### ① マイグレーションファイルを作成する場合

```
docker compose exec app poetry run alembic revision --autogenerate -m "create tables"
```

app/db/versions に migration ファイル作成

##### ② 作成したマイグレーションファイルを適用(必ず migration を実施したあと、実行)

```
docker compose exec app poetry run alembic upgrade head
```

### Pytestによるテスト

#### testの実行方法
すべてのtestが実行されます.(現在は、test\api\test_recognize_info.pyのみ)
```
docker-compose run --entrypoint "poetry run pytest" app
```


### 停止

アプリケーションを停止する場合は、以下のコマンドを実行

```
docker compose down
```
