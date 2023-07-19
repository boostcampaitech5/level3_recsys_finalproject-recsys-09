from fastapi import APIRouter, Request, Depends
import uuid
from schemas.response import BaseResponse
from schemas.request import FeedbackRequest
from core.preload import get_template

home_router = APIRouter(prefix="/home")

@home_router.post("/")
def home_page(request: Request,  feedback: FeedbackRequest = Depends(FeedbackRequest.as_form)):
    
    templates =  get_template()
    print(feedback)
    
    return templates.TemplateResponse("main.html", BaseResponse(request=request).__dict__)


@home_router.get("/")
def home_page(request: Request):
    """
        시작 화면을 return한다.
    """
    
    templates = get_template()
    
    response = templates.TemplateResponse("main.html", BaseResponse(request=request).__dict__)
    
    cookie_id = request.cookies.get("id")
    
    if not cookie_id:
        cookie_id = str(uuid.uuid4())
        response.set_cookie(key="id", value=cookie_id, httponly=True)
    
    return response