from typing import Callable

from fastapi import FastAPI
from sqlalchemy import create_engine
from core.config import POSTGRE, MODEL_IP, REDIS_PORT
import pandas as pd
from direct_redis import DirectRedis

import os

redis_client = DirectRedis(host=MODEL_IP, port=REDIS_PORT)
# redis_client = DirectRedis(host="localhost", port=REDIS_PORT)

def redis_use():
    # Create a sample DataFrame
    engine = create_engine(POSTGRE)
    game_table = pd.read_sql_table(table_name="game", con=engine)
    cb_model_table = pd.read_sql_table(table_name="cb_model", con=engine)
    Ease_table = pd.read_sql_table(table_name="Ease", con=engine)
    cf_table = pd.read_sql_table(table_name="cf_model", con=engine)

    # Store DataFrame data in Redis with a key (e.g., 'df_cache')
    redis_client.set('game', game_table)
    redis_client.set('cb_model', cb_model_table)
    redis_client.set('Ease', Ease_table)
    redis_client.set('cf_model', cf_table)

    details_table = pd.read_sql_table(table_name="details", con=engine)
    redis_client.set('details', details_table)
