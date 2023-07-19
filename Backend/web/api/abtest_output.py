from fastapi import APIRouter, Request, Depends
from schemas.response import ABOutputResponse
from schemas.request import UserRequest, CBRequest, GPTRequest
from core.preload import get_template
from core.output_process import get_response, ab_create_response

output_router = APIRouter(prefix="/output")

@output_router.post("/")
def output_page(request: Request, user: UserRequest = Depends(UserRequest.as_form)):
    """
    user에게 받은 input을 model의 input으로 넘겨주고 추천 game을 받아 output page를 return한다.
    
    기능
    1. 모델 서버로 output 요청하기
    2. 모델 서버로부터 받은 output과 db를 이용해 사용자에게 제공할 game list 생성 (DB)
    3. html로 추천 game list를 전달한다.
    4. 모델 서버로 보낸 input과 모델 서버로부터 받은 output을 logging한다. (선택)
    """
    
    templates = get_template()
    
    # model server로 request 보내기
    cb_model = get_response(CBRequest, user, 'cb_model')
    gpt = get_response(GPTRequest, user, 'gpt')
    cf_model = get_response(CBRequest, user, 'cf_model')
    
    # model server response 처리를 통한 추천 game list 생성
    cb_dic = ab_create_response(cb_model, "cb", "id")
    gpt_dic = ab_create_response(gpt, "gpt", "name")
    cf_dic = ab_create_response(cf_model, "cf","id")

    return templates.TemplateResponse("outputdemo.html", ABOutputResponse(request=request, cb_model=cb_dic, gpt=gpt_dic, cf_model=cf_dic).__dict__)