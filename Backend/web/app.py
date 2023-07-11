from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from data_class import RecommendedGame
import uvicorn


app = FastAPI()
templates = Jinja2Templates(directory="../../Frontend")


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
        
    game_list = ["Zombie Driver: Immortal Edition", "Zumba Fitness Rush"]

    return templates.TemplateResponse("input.html", {"request": request, "game_list": game_list})


@app.post("/output")
async def output_page(request: Request):#, user: UserInfo):
    """
    user에게 받은 input을 model의 input으로 넘겨주고 추천 game을 받아 output page를 return한다.
    
    기능
    1. 모델 서버로 output 요청하기
    2. 모델 서버로부터 받은 output과 db를 이용해 사용자에게 제공할 game list 생성 (DB)
    3. html로 추천 game list를 전달한다.
    4. 모델 서버로 보낸 input과 모델 서버로부터 받은 output을 logging한다. (선택)
    
    """
    age = "20"
    machine = ["PC", "PS4"]
    players = "1"
    genre = ["Action", "Adventure"]
    tag = ["sound", "hard"]
    games = ["Zombie Driver: Immortal Edition", "Zumba Fitness Rush"]
    
    
    # content based model input
    cb_input = {
        "age": int(age),
        "platform": machine,
        "players": int(players),
        "games": games
    }
    
    # gpt input
    gpt_input = {
        "age": int(age),
        "platform": machine,
        "players": int(players),
        "games": games
    }
    
    game_list = ["Zombie Driver: Immortal Edition", "Zumba Fitness Rush"]
    url_list = ["url1", "url2"]
    
    output = {
        "games": game_list,
        "urls": url_list
    }
    return templates.TemplateResponse("test.html", {"request": request, "game": RecommendedGame(**output)})

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)