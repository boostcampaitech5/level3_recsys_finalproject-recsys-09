from fastapi import APIRouter, Request, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from schemas.response import OutputResponse
from schemas.request import UserRequest, ModelRequest, GPTRequest
from core.preload import get_template
from core.output_process import get_response, create_response
from core.save_db import save_user_info, save_model_output
from database.db import get_db2

output_router = APIRouter(prefix="/output")

@output_router.post("/")
async def output_page(request: Request, background_tasks: BackgroundTasks, user: UserRequest = Depends(UserRequest.as_form), db: Session = Depends(get_db2)):
    """
    user에게 받은 input을 model의 input으로 넘겨주고 추천 game을 받아 output page를 return한다.
    
    기능
    1. 모델 서버로 output 요청하기
    2. 모델 서버로부터 받은 output과 db를 이용해 사용자에게 제공할 game list 생성 (DB)
    3. html로 추천 game list를 전달한다.
    4. 모델 서버로 보낸 input과 모델 서버로부터 받은 output을 logging한다. (선택)
    """
    
    templates =  get_template()
    id = save_user_info(user, db)
    
    # model server로 request 보내기
    hb_model = get_response(ModelRequest, user, 'hb_model')
    gpt = get_response(GPTRequest, user, 'gpt')
    background_tasks.add_task(save_model_output, id, gpt, 'gpt', db)
    background_tasks.add_task(save_model_output, id, hb_model, 'hb_model', db)
    
    # model server response 처리를 통한 추천 game list 생성
    game_dic = create_response(hb_model, gpt, user)
    
    response = templates.TemplateResponse("output.html", OutputResponse(request=request, games=game_dic).__dict__)
    response.set_cookie(key="id", value=id)

    return response