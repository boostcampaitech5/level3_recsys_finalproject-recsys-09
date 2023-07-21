from fastapi import FastAPI

from api.routes.api import router as api_router
from core.events import preload_db, is_csv_file_exists
from core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION, DATA_DIR, DB_DATA


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    application.include_router(api_router, prefix=API_PREFIX)
    pre_load = False
    # pre_load = is_csv_file_exists(DATA_DIR, DB_DATA)
    if pre_load:
        application.add_event_handler("startup", preload_db)
    return application


app = get_application()
