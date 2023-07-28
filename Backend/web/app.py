from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from api.home import home_router
from api.input import input_router
from api.output import output_router
from core.preload import preload
from core.config import HOST, PORT


app = FastAPI()
app.mount("/static", StaticFiles(directory="./Frontend"), name="static")

@app.get("/")
def redirect_home():
    return RedirectResponse(f"http://{HOST}:{PORT}/home")

if __name__ == '__main__':
    app.add_event_handler('startup', preload)
    app.include_router(home_router)
    app.include_router(input_router)
    app.include_router(output_router)
    uvicorn.run(app, host="0.0.0.0", port=8080)