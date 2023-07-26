import os

from loguru import logger

from core.errors import PredictException, ModelLoadException
from core.config import POSTGRE, API_KEY

# model
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import openai
# data
import pandas as pd
import numpy as np
import random
from services.filters import filter
from services.preprocess import * 


class HybridModel():
    def __init__(self, user_data):
        self.user_games_id = user_data.games
        self.age = int(user_data.age)
        self.platform = user_data.platform
        self.players = int(user_data.players)
        self.major_genre = user_data.major_genre
        self.tag = tag_preprocessing(user_data.tag)

        self.initialize_data()
        self.preprocess()
    
    def initialize_data(self):
        self.game_table = load_data_from_redis('game')
        self.cb_table = load_data_from_redis('cb_model')
        self.model_table = load_data_from_redis('Ease')
        self.cf_table = load_data_from_redis('cf_model')
    
    def preprocess(self):
        # model_table preprocess
        # user_idx로 묶어서 id를 배열로 합치기
        self.cf_table = self.cf_table.groupby('user_idx')['id'].apply(list).reset_index()
        self.cf_table["id"] = self.cf_table["id"].apply(lambda x: np.array(x, dtype=int))

        # user game log preprocess
        self.df_user = user_game_log_preprocess(self.cb_table, self.tag, self.user_games_id)
        
    def cf_predict(self):
        self.cf_table['similarity'] = self.cf_table['id'].apply(lambda x: game_similarity(x, self.user_games_id))

        similarity_df = self.cf_table[self.cf_table['similarity'] == max(self.cf_table['similarity'])]
        similarity_df = select_similar_user(similarity_df)

        ease_predict = self.model_table[self.model_table['user'].isin(list(similarity_df['user_idx']))]

        self.combined_ids = similarity_df['id'].explode().tolist()
        self.combined_ids = self.combined_ids + list(ease_predict['item'])

    def cb_predict(self):
        # 사전에 입력받은 유저정보로 필터링
        idx = filter(self.game_table, self.age, self.platform, self.players, self.major_genre)
        filtered_df = self.cb_table[self.cb_table['id'].isin(self.combined_ids)]
        filtered_df = filtered_df[filtered_df['id'].isin(idx)]

        # 유사도 계산 시작 
        self.final_df = pd.concat([filtered_df, self.df_user], ignore_index=True)
        self.final_df = self.final_df.drop_duplicates(subset='id', keep='last') # 'id' 중복 제거, 중복이 있다면 뒤에 것을 남김

        # "genre" 열의 장르들을 숫자로 매핑
        vectorizer = CountVectorizer(tokenizer=lambda x: x.split(', '))
        genre_matrix = vectorizer.fit_transform(self.final_df['genre'])
        genre_df = pd.DataFrame(genre_matrix.toarray())

        numeric_df = self.final_df.drop(['id', 'genre'], axis=1) # "id" 열 제외

        # 숫자 데이터와 장르 데이터 결합
        if self.tag == -1:
            df_combined = genre_df
        else: df_combined = pd.concat([numeric_df, genre_df], axis=1)

        # 코사인 유사도 계산
        similarity_matrix = cosine_similarity(df_combined)

        # 유사도 행렬을 데이터프레임으로 변환
        similarity_df = pd.DataFrame(similarity_matrix, index=self.final_df.index, columns=self.final_df.index)

        # 상위 10개 유사한 항목 찾기
        item_id = 0  # 기준 항목의 인덱스
        similar_items = similarity_df[item_id].nlargest(len(self.df_user) + 10)[len(self.df_user):]  # 상위 10개 유사한 항목 (자기 자신 제외)

        # 상위 10개 유사한 항목의 인덱스
        similar_item_ids = similar_items.index.tolist()

        # 추천 게임 목록 생성
        self.recommendations = self.final_df.loc[similar_item_ids, 'id'].tolist()

    def predict(self):
        if not self.user_games_id:
            return []
        
        self.cf_predict()
        self.cb_predict()

        return self.recommendations

class Most_popular_filter():
    def __init__(self, user_data):
        self.age = int(user_data.age)
        self.platform = user_data.platform
        self.players = int(user_data.players)
        self.major_genre = user_data.major_genre

        self.initialize_data()
        self.preprocess_input()
        
    def initialize_data(self):
        self.game_table = load_data_from_redis('game')
        self.details_table = load_data_from_redis('details')

    def preprocess_input(self):
        # 필터링
        self.idx = filter(self.game_table, self.age, self.platform, self.players, self.major_genre)

    def predict(self):
        self.details_table = self.details_table[self.details_table['id'].isin(self.idx)]
        self.details_table = self.details_table.sort_values(by="critic_score", ascending=False)
        return list(self.details_table.head(10)['id'])

def chatGPT(user_data):
    # set api key
    openai.api_key = API_KEY 

    if user_data.players == "0" and len(user_data.tag) == 0:
        message = "{}살이상이고 {}를 가지고 있고 {} 장르를 선호해 해본 게임은 {}야".format(user_data.age, user_data.platform, user_data.major_genre, user_data.games)
    elif user_data.players == "0":
        message = "{}살이상이고 {}를 가지고 있고 {} 장르와 {} 부분을 고려한 게임을 선호해 해본 게임은 {}야".format(user_data.age, user_data.platform, user_data.major_genre, user_data.tag, user_data.games)
    elif len(user_data.tag) == 0:
        message = "{}살이상이고 {}를 가지고 있고 {} 장르와 {}인용 게임를 선호해. 해본 게임은 {}야".format(user_data.age, user_data.platform, user_data.major_genre, user_data.players, user_data.games)
    else:
        message = "{}살이상이고 {}를 가지고 있고 {} 장르와 {} 부분을 고려한 {}인용 게임를 선호해. 해본 게임은 {}야".format(user_data.age, user_data.platform, user_data.major_genre, user_data.tag, user_data.players, user_data.games)

    # Call the chat GPT API
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"게임을 플레이한 유저의 정보를 보여줄테니까 이 정보를 바탕으로 게임 10개를 이름만 추천해줘"},
            {"role": "system", "content": f"게임의 영어 정식 명칭으로 추천 해주고 유저가 이미 플레이 한 게임은 추천하지 말아줘."},
            {"role": "assistant", "content": f"다음 예시와 같이 대답해줘. 1. 게임1 2. 게임2 3. 게임3 4. 게임4 5. 게임5 6. 게임6 7. 게임7 8. 게임8 9. 게임9 10. 게임10"},
            {"role": "user", "content": message}
        ],
        temperature=0,
        max_tokens=100
    )
    return completion['choices'][0]['message']['content']