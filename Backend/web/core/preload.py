from fastapi import Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session
from database.db import get_db

game_list = []
templates = None

def preload(db: Session = Depends(get_db)):
    global templates
    templates = Jinja2Templates(directory="./Frontend")
    
    global game_list
    with get_db() as con:
        statement = text("""select name from game order by name asc""")
        result = con.execute(statement)
        
    game_list.extend([rs[0].lower() for rs in result])

def get_game_list():
    global game_list
    return game_list

def get_template():
    global templates
    return templates
    