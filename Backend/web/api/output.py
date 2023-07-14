from fastapi import APIRouter, Request, Depends
from sqlalchemy import bindparam, text
from sqlalchemy.orm import Session
import requests
import os
from schemas.data_class import RecommendedGame
from database.db import get_db
from core.preload import get_template

output_router = APIRouter(prefix="/output")

@output_router.post("/")
async def output_page(request: Request, db: Session = Depends(get_db)):
    """
    user에게 받은 input을 model의 input으로 넘겨주고 추천 game을 받아 output page를 return한다.
    
    기능
    1. 모델 서버로 output 요청하기
    2. 모델 서버로부터 받은 output과 db를 이용해 사용자에게 제공할 game list 생성 (DB)
    3. html로 추천 game list를 전달한다.
    4. 모델 서버로 보낸 input과 모델 서버로부터 받은 output을 logging한다. (선택)
    """
    
    templates =  get_template()
    
    form_data = await request.form()
    
    age = form_data.get("age")
    if int(age) == 0:
        young = form_data.get("young")
        age = young
    platform = form_data.getlist("platform")
    players = form_data.get("players")
    genre = form_data.getlist("genre")
    tag = form_data.getlist("tag") # 긍정 0, 부정 1, 쉬움 1, 어려움 2
    games = form_data.getlist("search")
    
    
    # content based model input
    cb_input = {
        'age': age,
        'platform': platform,
        'players': players,
        'major_genre': genre,
        'tag': tag,
        'games': games
    }
    
    # gpt input
    gpt_input = {
        'age': age,
        'platform': platform,
        'players': players,
        'games': games
    }

    print(cb_input, gpt_input)
    #model server로 request 보내기
    cb_response = requests.post(f"http://{os.environ['MODEL_HOST']}:{os.environ['MODEL_PORT']}/api/cb_model/predict", json=cb_input)
    gpt_response = requests.post(f"http://{os.environ['MODEL_HOST']}:{os.environ['MODEL_PORT']}/api/gpt/predict", json=gpt_input)
    
    print(cb_response.json(), gpt_response.json())
    cb_model= cb_response.json()['games']
    gpt = gpt_response.json()['games']
    
    # model server response 처리
    game_list = []
    url_list = []
    
    with get_db() as con:
        for title in gpt:
            title_param = bindparam("title", title)
            
            statement = text("select name, img_url from game where name=:title")
            statement = statement.bindparams(title_param)
            gpt_result = con.execute(statement)
            
            for rs in gpt_result:
                if len(game_list) == 4:
                    break
                game_list.append(rs[0])
                url_list.append(rs[1])
        
        for id in cb_model:
            statement = text(f"select name, img_url from game where id={id}")
            cb_result = con.execute(statement)
            
            for rs in cb_result:
                if len(game_list) == 5:
                    break
                game_list.append(rs[0])
                url_list.append(rs[1])
    
    output = {
        "games": game_list,
        "urls": url_list
    }
    
    return templates.TemplateResponse("output.html", {"request": request, "game": RecommendedGame(**output), "ip": os.environ['HOST'], "port": os.environ['PORT']})

