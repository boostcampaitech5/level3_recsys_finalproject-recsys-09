from typing import Callable

from fastapi import FastAPI
from sqlalchemy import create_engine
from core.config import POSTGRE, MODEL_IP, REDIS_PORT, JSON_PATH
import pandas as pd
from direct_redis import DirectRedis

import glob
from google.cloud import bigquery
from google.oauth2 import service_account

import os

def read_bigquery(table_name):
    # Credentials 객체 생성
    credentials = service_account.Credentials.from_service_account_file(JSON_PATH)

    # GCP 클라이언트 객체 생성
    client = bigquery.Client(credentials = credentials, 
                            project = credentials.project_id)

    # 데이터 조회 쿼리
    sql = """
    SELECT
    *
    FROM
    test_game_total.{}
    """.format(table_name)

    # 데이터 조회 쿼리 실행 결과
    query_job = client.query(sql)

    # 데이터프레임 변환
    df = query_job.to_dataframe()
    if 'id' in df.columns:
        df['id'] = df['id'].astype('int64')
    return df

import os

redis_client = DirectRedis(host=MODEL_IP, port=REDIS_PORT)

def redis_use():
    # read by bigquery
    game_table = read_bigquery("game")
    cb_model_table = read_bigquery("cb_model")
    Ease_table = read_bigquery("ease")
    cf_table = read_bigquery("cf_model")
    details_table = read_bigquery("details")

    # Store DataFrame data in Redis with a key (e.g., 'df_cache')
    redis_client.set('game', game_table)
    redis_client.set('cb_model', cb_model_table)
    redis_client.set('Ease', Ease_table)
    redis_client.set('cf_model', cf_table)
    redis_client.set('details', details_table)
