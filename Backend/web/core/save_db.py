from google.cloud import bigquery
from sqlalchemy import text, bindparam
from database.db import get_db2


def save_user_info(id, user, client):
    sql = """
    INSERT INTO review.user_info (id, age, platform, players, major_genre, tag, games)
    VALUES (@id, @age, @platform, @players, @major_genre, @tag, @games)
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("id", "STRING", id),
            bigquery.ScalarQueryParameter("age", "INT64", int(user.age)),
            bigquery.ArrayQueryParameter("platform", "STRING", user.platform),
            bigquery.ScalarQueryParameter("players", "INT64", int(user.players)),
            bigquery.ArrayQueryParameter("major_genre", "STRING", user.major_genre),
            bigquery.ArrayQueryParameter("tag", "STRING", user.tag),
            bigquery.ArrayQueryParameter("games", "STRING", user.games)
        ]
    )
    client.query(sql, job_config=job_config).result()


def save_model_output(id, hb_model, gpt, client):

    sql_hb = f"""
    INSERT INTO review.hb_output (id, games)
    VALUES (@id, @games)
    """
    job_config_hb = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("id", "STRING", id),
            bigquery.ArrayQueryParameter("games", "INT64", hb_model)
        ]
    )
    client.query(sql_hb, job_config=job_config_hb).result()
    
    sql_gpt = f"""
    INSERT INTO review.gpt_output (id, games)
    VALUES (@id, @games)
    """
    job_config_gpt = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("id", "STRING", id),
            bigquery.ArrayQueryParameter("games", "STRING", gpt)
        ]
    )
    client.query(sql_gpt, job_config=job_config_gpt).result()
    
        
def save_feedback(id, feedback):
    with get_db2() as con:
        params = [bindparam("id", id), bindparam("cb_model", [int(id) for id in feedback.cblike]), \
            bindparam("gpt", [int(id) for id in feedback.gptlike]), bindparam("cf_model", [int(id) for id in feedback.cflike])]
        statement = text("""insert into feedback (id, cb_model, gpt, cf_model)
                         values (:id, :cb_model, :gpt, :cf_model)""")
        
        statement = statement.bindparams(*params)
        con.execute(statement)
        con.commit()