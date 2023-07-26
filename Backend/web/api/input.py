from fastapi import APIRouter, Request
from core.preload import get_game_list, get_template
from schemas.response import InputResponse

input_router = APIRouter(prefix="/input")

@input_router.get("/")
def input_page(request: Request):
    """
        정보 입력 화면을 return한다.
        
        html로 선택할 수 있는 게임 리스트를 전달한다. (DB)
    """
    
    game_list = get_game_list()
    templates = get_template()
    
    response = templates.TemplateResponse("input.html", InputResponse(request=request, game_list=game_list).__dict__)
    
    return response