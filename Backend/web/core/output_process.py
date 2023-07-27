from sqlalchemy import bindparam, text
import requests
from database.db import get_db
from schemas.request import ModelRequest
from core.config import MODEL_HOST, MODEL_PORT


def get_response(model, user, api):
    input = model(**user.__dict__)
    
    if api == "hb_model" and not input.games:
        return []
        
    response = requests.post(f"http://{MODEL_HOST}:{MODEL_PORT}/api/{api}/predict", json=input.__dict__)
    
    try:
        response.raise_for_status()
    except:
        return []
    
    return response.json()['games']


def create_response(hb_model, gpt, user):
    game_id = []
    
    gpt = search_games(gpt)
    
    lst1, lst2 = gpt, hb_model
    if not lst1: 
        lst1, lst2 = lst2, lst1
    
    while len(game_id) < 8 and lst1:
        while lst1 and (lst1[0] in game_id):
            lst1.pop(0)
        if lst1:
            game_id.append(lst1.pop(0))
        if lst2:
            if lst1 and len(game_id) >= 7:
                continue
            lst1, lst2 = lst2, lst1

    if len(game_id) < 8:
        popular = get_response(ModelRequest, user, 'popular')
        while len(game_id) < 8 and popular:
            while popular and (popular[0] in game_id):
                popular.pop(0)
            if popular:
                game_id.append(popular.pop(0))
            
    game_dic = {}
    
    with get_db() as con:
        for idx, id in enumerate(game_id):
            param = bindparam("id", id)
            statement = text(f"""select a.id, a.name, b.url, a.img_url, a.platform, a.major_genre
                                from (select id, name, img_url, platform, major_genre from game where id = :id) a
                                inner join details b
                                on a.id = b.id""")
            statement = statement.bindparams(param)
            result = con.execute(statement)
            
            for rs in result:
                game_info = [elem for elem in rs]
                game_info[2] = game_info[2].split(',')[0].strip()[1:-1]
                game_dic[idx] = game_info
    
    return game_dic


def search_games(games):
    filter_games = []
    
    with get_db() as con:
            for game in games:
                param = bindparam("game", game.replace(' ', ''))
                statement = text("""select id, name from game where REPLACE(name, ' ',  '')
                                 ilike :game""")
                statement = statement.bindparams(param)
                result = con.execute(statement)
                
                for rs in result:
                    filter_games.append(rs[0])
                    
    return filter_games


def ab_create_response(model, name, type):
    game_list = []
    game_dic = {}
    dic_len = 0
    
    with get_db() as con:
        for game in model:
            param = bindparam(type, game)
            statement = text(f"select id, name, img_url, platform from game where {type}=:{type}")
            statement = statement.bindparams(param)
            result = con.execute(statement)
            
            for rs in result:
                if dic_len == 3:
                    break
                game_dic[f'{name}{dic_len}'] = rs
                game_list.append(rs[0])
                dic_len += 1
    
    return game_list, game_dic