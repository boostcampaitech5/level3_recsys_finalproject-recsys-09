from sqlalchemy import text, bindparam


def save_user_info(user, db):
    params = [bindparam("age", int(user.age)), bindparam("platform", user.platform), bindparam("players", int(user.players)), \
        bindparam("major_genre", user.major_genre), bindparam("tag", user.tag), bindparam("games", user.games)]
    statement = text("""insert into user_info (age, platform, players, major_genre, tag, games)
                        values (:age, :platform, :players, :major_genre, 
                        :tag, :games) returning id""")
    statement = statement.bindparams(*params)
    
    result = db.execute(statement)
    
    for rs in result:
        id = rs[0]
        
    db.commit()
        
    return id


def save_model_output(id, games, tb_name, db):
    params = [bindparam("id", id), bindparam("games", games)]
    statement = text(f"""insert into {tb_name}_output (id, games)
                    values (:id, :games)""")
    
    statement = statement.bindparams(*params)
    
    db.execute(statement)
    db.commit()
        
        
def save_feedback(id, feedback, db):
    params = [bindparam("id", id), bindparam("likes", [int(id) for id in feedback.like])]
    statement = text("""insert into final_feedback (id, likes)
                        values (:id, :likes)""")
    
    statement = statement.bindparams(*params)
    db.execute(statement)
    db.commit()