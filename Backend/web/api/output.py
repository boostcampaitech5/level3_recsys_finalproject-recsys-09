from fastapi import APIRouter, Request, Depends
from schemas.response import OutputResponse, BaseResponse
from schemas.request import UserRequest, ModelRequest, GPTRequest, FeedbackRequest
from core.preload import get_template
from core.output_process import get_response, create_response

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
    
    templates =  get_template()
    
    # model server로 request 보내기
    hb_model = get_response(ModelRequest, user, 'hb_model')
    gpt = get_response(GPTRequest, user, 'gpt')
    
    # model server response 처리를 통한 추천 game list 생성
    game_dic = create_response(hb_model, gpt, user)

    return templates.TemplateResponse("output.html", OutputResponse(request=request, games=game_dic).__dict__)


@output_router.post("/feedback")
def get_feedback(request: Request, feedback: FeedbackRequest = Depends(FeedbackRequest.as_form)):
    
    templates =  get_template()
    
    print(feedback)
    return templates.TemplateResponse("main.html", BaseResponse(request=request).__dict__)

