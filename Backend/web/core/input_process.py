from sqlalchemy import bindparam, text
from database.db import get_db


def search_games_model(games):
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


def search_games_gpt(games):
    filter_games = []
    
    with get_db() as con:
        for game in games:
            if game == '':
                continue
            
            param = bindparam("game", game.replace(' ', ''))
            statement = text("""select id, name from game where REPLACE(name, ' ',  '')
                                ilike :game""")
            statement = statement.bindparams(param)
            result = con.execute(statement)
            rows = result.fetchall()
            
            if rows:
                for r in rows:
                    filter_games.append(r[1])
            else:
                filter_games.append(game)
    return filter_games