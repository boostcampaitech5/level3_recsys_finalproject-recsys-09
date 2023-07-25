from google.cloud import bigquery
from database.bigquery import get_bigquery_client

def search_games_model(games):
    client = get_bigquery_client()
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


def search_games_gpt(games):
    client = get_bigquery_client()
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
        result = list(client.query(sql, job_config=job_config).result())
        if not result:
            filter_games.append(game)
        else:
            for rs in result:
                filter_games.append(rs[1])
    
    return filter_games