from fastapi import Depends
from sqlalchemy import text, bindparam
from sqlalchemy.orm import Session
from database.db import get_db2

def save_user_info(user, db: Session = Depends(get_db2)):
    with get_db2() as con:
        params = [bindparam("age", int(user.age)), bindparam("platform", user.platform), bindparam("players", int(user.players)), \
            bindparam("major_genre", user.major_genre), bindparam("tag", user.tag), bindparam("games", user.games)]
        statement = text("""insert into user_info (age, platform, players, major_genre, tag, games)
                            values (:age, :platform, :players, :major_genre, 
                            :tag, :games) returning id""")
        statement = statement.bindparams(*params)
        
        result = con.execute(statement)
        
        for rs in result:
            id = rs[0]
        
        con.commit()
        
    return id

def save_model_output(id, cb_dic, gpt_dic, cf_dic, db: Session = Depends(get_db2)):
    with get_db2() as con:
        for output in [cb_dic, gpt_dic, cf_dic]:
            params = [bindparam("id", id), bindparam("games", output)]
            statement = text("""insert into cb_model_output (id, games)
                            values (:id, :games)""")
            
            statement = statement.bindparams(*params)
            
            con.execute(statement)
        con.commit()