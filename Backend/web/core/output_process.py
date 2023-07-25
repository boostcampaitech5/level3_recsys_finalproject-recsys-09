from google.cloud import bigquery
import requests
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


def create_response(hb_model, gpt, user, client):
    game_id = []
    
    gpt = search_games(gpt, client)
    for id in gpt:
        if len(game_id) == 6:
            break
        
        if id in game_id:
            continue
        
        game_id.append(id)
        
    for id in hb_model:
        if len(game_id) == 10:
            break
        
        if id in game_id:
            continue
        
        game_id.append(id)
    
    if len(game_id) < 10:
        popular = get_response(ModelRequest, user, 'popular')
        for id in popular:
            if len(game_id) == 10:
                break
            
            if id in game_id:
                continue
            
            game_id.append(id)
            
    game_dic = {}
    
    sql = """
    SELECT a.id, a.name, b.url, a.img_url, a.platform, a.major_genre
    FROM test_game_total.game a 
    JOIN test_game_total.details b ON a.id = b.id
    WHERE a.id IN UNNEST(@game_id)
    """
    job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ArrayQueryParameter("game_id", "INT64", game_id)
        ]
    )
    result = client.query(sql, job_config=job_config).result()
    
    for idx, rs in enumerate(result):
        game_info = [elem for elem in rs[:6]]
        game_info[2] = game_info[2].split(',')[0].strip()[1:-1]
        game_dic[idx] = game_info
    
    return game_dic


def search_games(games, client):
    filter_games = []
    
    for game in games:
        sql = """
        SELECT id, name
        FROM test_game_total.game 
        WHERE REPLACE(LOWER(name), ' ', '') = @game;
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
            bigquery.ScalarQueryParameter("game", "STRING", game.lower().replace(' ', ''))
            ]
        )
        result = client.query(sql, job_config=job_config).result()
        for rs in result:
            filter_games.append(rs[0])
                
    return filter_games


# def ab_create_response(model, name, type, db: Session = Depends(get_db)):
#     game_list = []
#     game_dic = {}
#     dic_len = 0
    
#     with get_db() as con:
#         for game in model:
#             param = bindparam(type, game)
#             statement = text(f"select id, name, img_url, platform from game where {type}=:{type}")
#             statement = statement.bindparams(param)
#             result = con.execute(statement)
            
#             for rs in result:
#                 if dic_len == 3:
#                     break
#                 game_dic[f'{name}{dic_len}'] = rs
#                 game_list.append(rs[0])
#                 dic_len += 1
    
#     return game_list, game_dic