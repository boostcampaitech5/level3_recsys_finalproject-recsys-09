from core.errors import PredictException, ModelLoadException
from core.config import POSTGRE, MODEL_IP, REDIS_PORT

import random
import pandas as pd
from sqlalchemy import create_engine
from direct_redis import DirectRedis
redis_client = DirectRedis(host=MODEL_IP, port=REDIS_PORT)


def tag_preprocessing(tags):
    tag_list = ['Graphics', 'Sound', 'Creativity', 'Freedom', 'Hitting', 'Completion', 'easy', 'hard']
    user_tag = [2 if i == 'hard' else 1 if i in tags else 0 for i in tag_list]
    return user_tag if len(tags) > 0 else -1

def load_data_from_redis(key):
    if key not in redis_client:
        engine = create_engine(POSTGRE)
        table = pd.read_sql_table(table_name=key, con=engine)
        redis_client.set(key, table)
    return redis_client.get(key)

def user_game_log_preprocess(cb_table, tag, user_games_id):
    if tag == -1: columns=['id', 'genre']
    else: columns = ['id', 'genre', 'graphics', 'sound', 'creativity', 'freedom', 'hitting', 'completion', 'difficulty']
    
    df_user = pd.DataFrame(columns=columns)

    for i in user_games_id:
        input_df =  cb_table[cb_table['id']== i]
        df_user = pd.concat([df_user, input_df[['id', 'genre']]], ignore_index=True)
    
    # tag 정보가 있을때
    if tag != -1:
        df_user = df_user.fillna(dict(zip(df_user.columns[2:], tag)))
    
    return df_user

def game_similarity(arr1, arr2):
    set1 = set(arr1)
    set2 = set(arr2)

    intersection = set1.intersection(set2)
    return len(intersection)

def select_similar_user(df):
    if len(df) > 3:
        df.loc[:, 'id'] = df['id'].apply(lambda x: x[:5])
    return df

def select_similar_user_idx(df):
    if len(df) <= 3:
        return list(df['user_idx'])
    else:
        return random.sample(list(df['user_idx']), 3)