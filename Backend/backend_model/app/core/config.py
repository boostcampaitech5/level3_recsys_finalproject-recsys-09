import sys
import logging

from loguru import logger
from starlette.config import Config
from starlette.datastructures import Secret

from core.logging import InterceptHandler

config = Config(".env")

API_PREFIX = "/api"
VERSION = "0.1.0"
DEBUG: bool = config("DEBUG", cast=bool, default=False)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret, default="")

PROJECT_NAME: str = config("PROJECT_NAME", default="Backend Model")

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

MODEL_PATH = config("MODEL_PATH", default="./ml/model/")
MODEL_NAME = config("MODEL_NAME", default="model.pkl")
INPUT_EXAMPLE = config("INPUT_EXAMPLE", default="./ml/model/examples/example.json")
POSTGRE = config("POSTGRE", default="")
API_KEY = config("API_KEY", default="")
MODEL_IP = config("MODEL_IP", default="")
REDIS_PORT = config("REDIS_PORT", default="6379")
JSON_PATH = config("JSON_PATH", default="/app/app/bigquery.json")