from fastapi import APIRouter, Request
import os
from core.preload import get_template

home_router = APIRouter(prefix="/home")

@home_router.get("/")
def home_page(request: Request):
    """
        시작 화면을 return한다.
    """
    
    templates = get_template()
    
    return templates.TemplateResponse("main.html", {"request": request, "ip": os.environ['HOST'], "port": os.environ['PORT']})