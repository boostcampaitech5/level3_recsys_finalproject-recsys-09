from fastapi import Depends
from sqlalchemy import bindparam, text
from sqlalchemy.orm import Session
import requests
from database.db import get_db
from core.config import MODEL_HOST, MODEL_PORT

def get_response(model, user, api):
    input = model(**user.__dict__)
    
    response = requests.post(f"http://{MODEL_HOST}:{MODEL_PORT}/api/{api}/predict", json=input.__dict__)
    
    return response.json()['games']


def create_response(cb_model, gpt, db: Session = Depends(get_db)):
    game_dic = {}
    dic_len = 0
    
    with get_db() as con:
        for title in gpt:
            title_param = bindparam("title", title)
            
            statement = text("select name, img_url, platform from game where name=:title")
            statement = statement.bindparams(title_param)
            gpt_result = con.execute(statement)
            
            for rs in gpt_result:
                if dic_len == 4:
                    break
                game_dic[dic_len] = rs
                dic_len += 1
        
        for id in cb_model:
            statement = text(f"select name, img_url, platform from game where id={id}")
            cb_result = con.execute(statement)
            
            for rs in cb_result:
                if dic_len == 5:
                    break
                game_dic[dic_len] = rs
                dic_len += 1
    
    return game_dic
