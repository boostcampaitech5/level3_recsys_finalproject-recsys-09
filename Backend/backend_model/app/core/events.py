from typing import Callable

from fastapi import FastAPI
from sqlalchemy import create_engine
from core.config import POSTGRE
import pandas as pd

import os

def is_csv_file_exists(directory_path, filename):
    # 디렉토리의 파일 리스트를 가져옴
    files = os.listdir(directory_path)

    # 파일 리스트에서 주어진 파일명과 일치하는 파일이 있는지 확인
    for file in files:
        if file == filename:
            return False

    # 일치하는 파일이 없는 경우 False를 반환
    return True

def preload_db():
    engine = create_engine(POSTGRE)
    game_table = pd.read_sql_table(table_name="game", con=engine)
    cb_model_table = pd.read_sql_table(table_name="cb_model", con=engine)
    game_table.to_csv("./data/game_table.csv", index=False)
    cb_model_table.to_csv("./data/cb_model_table.csv", index=False)
