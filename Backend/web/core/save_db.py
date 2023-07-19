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

def save_model_output(id, cb_list, gpt_list, cf_list, db: Session = Depends(get_db2)):
    with get_db2() as con:
        for table, output in [("cb_model_output", cb_list), ("gpt_output", gpt_list), ("cf_model_output", cf_list)]:
            params = [bindparam("id", id), bindparam("games", output)]
            statement = text(f"""insert into {table} (id, games)
                            values (:id, :games)""")
            
            statement = statement.bindparams(*params)
            
            con.execute(statement)
        con.commit()
        
def save_feedback(id, feedback):
    with get_db2() as con:
        params = [bindparam("id", id), bindparam("cb_model", [int(id) for id in feedback.cblike]), \
            bindparam("gpt", [int(id) for id in feedback.gptlike]), bindparam("cf_model", [int(id) for id in feedback.cflike])]
        statement = text("""insert into feedback (id, cb_model, gpt, cf_model)
                         values (:id, :cb_model, :gpt, :cf_model)""")
        
        statement = statement.bindparams(*params)
        con.execute(statement)
        con.commit()