from fastapi import APIRouter, Request, Depends, BackgroundTasks
from google.cloud import bigquery
from schemas.response import BaseResponse
from schemas.request import GameFeedbackRequest
from core.preload import get_template
from core.save_db import save_feedback
from database.bigquery import get_bigquery_client

home_router = APIRouter(prefix="/home")

@home_router.post("/")
async def home_page(request: Request,  background_tasks: BackgroundTasks, feedback: GameFeedbackRequest = Depends(GameFeedbackRequest.as_form), client: bigquery.Client = Depends(get_bigquery_client)):
    
    templates =  get_template()
    
    id = request.cookies.get("id")
    background_tasks.add_task(save_feedback, id, feedback, client)
    
    return templates.TemplateResponse("main.html", BaseResponse(request=request).__dict__)


@home_router.get("/")
def home_page(request: Request):
    """
        시작 화면을 return한다.
    """
    
    templates = get_template()
    
    response = templates.TemplateResponse("main.html", BaseResponse(request=request).__dict__)
    
    return response