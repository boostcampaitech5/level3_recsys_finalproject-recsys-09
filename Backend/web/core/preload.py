from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from database.db import get_db

game_list = []
templates = None

def preload():
    global templates
    templates = Jinja2Templates(directory="./Frontend")
    
    global game_list
    with get_db() as con:
        statement = text("""select name from game order by name asc""")
        result = con.execute(statement)
    
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
    