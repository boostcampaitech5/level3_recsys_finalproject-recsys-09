from fastapi import APIRouter, Request
from core.preload import get_template
from schemas.response import BaseResponse

home_router = APIRouter(prefix="/home")

@home_router.get("/")
def home_page(request: Request):
    """
        시작 화면을 return한다.
    """
    
    templates = get_template()
    
    return templates.TemplateResponse("main.html", BaseResponse(request=request).__dict__)