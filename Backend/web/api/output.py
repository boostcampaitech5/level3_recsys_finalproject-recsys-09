from fastapi import APIRouter, Request, Depends
import uuid
from google.cloud import bigquery
from schemas.response import OutputResponse
from schemas.request import UserRequest, ModelRequest, GPTRequest
from core.preload import get_template
from core.save_db import save_user_info, save_model_output
from core.output_process import get_response, create_response
from database.bigquery import get_bigquery_client

output_router = APIRouter(prefix="/output")

@output_router.post("/")
def output_page(request: Request, user: UserRequest = Depends(UserRequest.as_form), client: bigquery.Client = Depends(get_bigquery_client)):
    """
    user에게 받은 input을 model의 input으로 넘겨주고 추천 game을 받아 output page를 return한다.
    
    기능
    1. 모델 서버로 output 요청하기
    2. 모델 서버로부터 받은 output과 db를 이용해 사용자에게 제공할 game list 생성 (DB)
    3. html로 추천 game list를 전달한다.
    4. 모델 서버로 보낸 input과 모델 서버로부터 받은 output을 logging한다. (선택)
    """
    
    templates = get_template()

    id = str(uuid.uuid4())
    save_user_info(id, user, client)
    
    # model server로 request 보내기
    hb_model = get_response(ModelRequest, user, 'hb_model')
    gpt = get_response(GPTRequest, user, 'gpt')
    save_model_output(id, hb_model, gpt, client)
    
    # model server response 처리를 통한 추천 game list 생성
    game_dic = create_response(hb_model, gpt, user)

    return templates.TemplateResponse("output.html", OutputResponse(request=request, games=game_dic).__dict__)