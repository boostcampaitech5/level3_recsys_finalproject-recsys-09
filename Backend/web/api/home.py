from fastapi import APIRouter, Request, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from schemas.response import BaseResponse
from schemas.request import GameFeedbackRequest
from core.preload import get_template
from core.save_db import save_feedback
from database.db import get_db2

home_router = APIRouter(prefix="/home")

@home_router.post("/")
async def home_page(request: Request, background_tasks: BackgroundTasks, feedback: GameFeedbackRequest = Depends(GameFeedbackRequest.as_form), db: Session = Depends(get_db2)):
    
    templates =  get_template()
    
    id = request.cookies.get("id")
    background_tasks.add_task(save_feedback, id, feedback, db)
    
    return templates.TemplateResponse("main.html", BaseResponse(request=request).__dict__)


@home_router.get("/")
def home_page(request: Request):
    """
        시작 화면을 return한다.
    """
    
    templates = get_template()
    
    response = templates.TemplateResponse("main.html", BaseResponse(request=request).__dict__)
    
    return response