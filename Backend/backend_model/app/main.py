from fastapi import FastAPI

from api.routes.api import router as api_router
from core.events import redis_use
from core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION, DATABASE


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    application.include_router(api_router, prefix=API_PREFIX)
    if DATABASE != 'False':
        application.add_event_handler("startup", redis_use)
    return application


app = get_application()