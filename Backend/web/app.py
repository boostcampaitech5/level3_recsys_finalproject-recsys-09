from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from data_class import RecommendedGame
import uvicorn
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="./Frontend"), name="static")
templates = Jinja2Templates(directory="./Frontend")
engine = create_engine(f"postgresql://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_DATABASE']}")

game_list = []

@app.on_event("startup")
def load_game_list():
    with engine.connect() as con:
        statement = text("""select name from game order by name asc""")
        result = con.execute(statement)
        
    game_list.extend([rs[0].lower() for rs in result])


@app.get("/")
def home_page(request: Request):
    """
        시작 화면을 return한다.
    """
    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/input")
def input_page(request: Request):
    """
        정보 입력 화면을 return한다.
        
        html로 선택할 수 있는 게임 리스트를 전달한다. (DB)
    """
    
    return templates.TemplateResponse("input.html", {"request": request, "game_list": game_list})


@app.post("/output")
async def output_page(request: Request):
    """
    user에게 받은 input을 model의 input으로 넘겨주고 추천 game을 받아 output page를 return한다.
    
    기능
    1. 모델 서버로 output 요청하기
    2. 모델 서버로부터 받은 output과 db를 이용해 사용자에게 제공할 game list 생성 (DB)
    3. html로 추천 game list를 전달한다.
    4. 모델 서버로 보낸 input과 모델 서버로부터 받은 output을 logging한다. (선택)
    """
    
    age = "20"
    platform = ["PC", "PS4"]
    players = "1"
    genre = ["Tactics", "Puzzle"]
    tag = ["Graphics", "Completion", "easy"] # 긍정 0, 부정 1, 쉬움 1, 어려움 2
    games = ["Zombie Driver: Immortal Edition", "Zumba Fitness Rush"]
    
    
    # content based model input
    cb_input = {
        "age": age,
        "platform": platform,
        "players": players,
        "major_genre": genre,
        "tag": tag,
        "games": games
    }
    
    # gpt input
    gpt_input = {
        "age": age,
        "platform": platform,
        "players": players,
        "games": games
    }

    #model server로 request 보내기
    cb_response = requests.post(f"http://{os.environ['MODEL_HOST']}:{os.environ['MODEL_PORT']}/api/cb_model/predict", json=cb_input)
    gpt_response = requests.post(f"http://{os.environ['MODEL_HOST']}:{os.environ['MODEL_PORT']}/api/gpt/predict", json=gpt_input)

    cb_model= cb_response.json()['games']
    gpt = gpt_response.json()['games']
    
    # model server response 처리
    game_list = []
    url_list = []
    
    with engine.connect() as con:
        for title in gpt:
            statement = text(f"select name, img_url from game where name='{title}'")
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
    
    return templates.TemplateResponse("output.html", {"request": request, "game": RecommendedGame(**output)})


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)