from typing import Optional
from fastapi import FastAPI, Form, Request
import uvicorn
import openai
from fastapi.templating import Jinja2Templates

from pathlib import Path
import os

from model import ContentBaseModel

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

print(BASE_DIR)

env_list = dict()

# 파일 경로
local_env = open(os.path.join(BASE_DIR, '.env'))

while True:
    line = local_env.readline()
    if not line:
        break
    line = line.replace('/n', '')
    start = line.find('=')
    key = line[:start]
    value = line[start+1:]
    env_list[key] = value

openai.api_key = env_list[key]

app = FastAPI()
templates = Jinja2Templates(directory='./')

@app.get("/message/")
def get_msg_form(request: Request):
    return templates.TemplateResponse('simple_input.html', context={'request': request})

@app.post("/message/")
def login(message: str = Form(...)):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": message}]
    )
    games = response.choices[0].message.content
    game_list = games.split("\n")  # 문자열을 줄바꿈("\n")을 기준으로 분리하여 리스트로 저장
    print(game_list)
    game_dict = {}

    for game in game_list:
        if game:
            key, value = game.split(". ")  # 앞의 숫자와 이름을 분리하여 key와 value로 저장
            game_dict[int(key)] = value  # 숫자를 정수로 변환하여 key로, 이름을 value로 딕셔너리에 추가

    return game_dict

@app.get("/model/")
def get_msg_form(request: Request):
    return templates.TemplateResponse('model_input.html', context={'request': request})

@app.post("/model/")
def login(user_games: list = Form(...)):
    model = ContentBaseModel(user_games)
    recommendations = model.predict()
    print(recommendations)
    game_dict = {}

    for i, game in enumerate(recommendations):
        if game:
            game_dict[i] = game  # 숫자를 정수로 변환하여 key로, 이름을 value로 딕셔너리에 추가

    return game_dict

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)