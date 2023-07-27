from starlette.config import Config

config = Config(".env")

HOST = config("HOST", default="")
PORT = config("PORT", default="")
DB_HOST = config("DB_HOST", default="")
DB_PORT = config("DB_PORT", default="")
DB_USERNAME = config("DB_USERNAME", default="")
DB_PASSWORD = config("DB_PASSWORD", default="")
DB_DATABASE = config("DB_DATABASE", default="")
DB_DATABASE_2 = config("DB_DATABASE_2", default="")
MODEL_HOST = config("MODEL_HOST", default="")
MODEL_PORT = config("MODEL_PORT", default="")