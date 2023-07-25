from fastapi.templating import Jinja2Templates
from database.bigquery import get_bigquery_client

game_list = []
templates = None

def preload():
    global templates
    templates = Jinja2Templates(directory="./Frontend")
    
    global game_list
    client = get_bigquery_client()
    sql ="""
    SELECT name from test_game_total.game
    """
    result = client.query(sql).result()
    game_list.extend([rs[0] for rs in result])

def get_game_list():
    global game_list
    if not game_list:
        preload()
    
    return game_list

def get_template():
    global templates
    if not templates:
        preload()
        
    return templates