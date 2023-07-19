# model
from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from sklearn.preprocessing import LabelEncoder
from multiprocessing import Pool, cpu_count
import random
# data
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
from src.filters import filter



class ContentBaseModel():
    def __init__(self, age, platform, players, major_genre, tag, user_games_names):
        self.user_games_names = list(user_games_names)
        self.age = age
        self.platform = platform
        self.players = players
        self.major_genre = major_genre
        self.tag = tag
        
        if self.tag[0] == -1: # tag 상관없음 처리
            self.tag = -1

        self.load_game_data()
        self.preprocess_input()
        self.filtering_data()
        

    def load_game_data(self):
        #engine = create_engine(POSTGRE)
        load_dotenv()
        engine = create_engine(f"postgresql://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_DATABASE']}")
        self.game_table = pd.read_sql_table(table_name="game", con=engine)
        self.model_table = pd.read_sql_table(table_name="cb_model", con=engine)

        if self.tag == -1:
            self.model_table = self.model_table[['id', 'genre']]

    def preprocess_input(self):
        if self.tag == -1:
            self.user_df = pd.DataFrame(columns=['id', 'genre'])
        else: 
            self.user_df = pd.DataFrame(columns=['id', 'genre', 'graphics', 'sound', 'creativity', 'freedom', 'hitting', 'completion', 'difficulty'])
        
        for i in self.user_games_names:
            input_idx = self.game_table[self.game_table['name'] == i].index
            input_df =  self.model_table.loc[input_idx]
            self.user_df = pd.concat([self.user_df, input_df[['id', 'genre']]], ignore_index=True)
            
        if self.tag != -1:
            self.user_df = self.user_df.fillna(dict(zip(self.user_df.columns[2:], self.tag)))

    def filtering_data(self):
        filtered_idx = filter(self.game_table, self.age, self.platform, self.players, self.major_genre, 'cb')
        self.model_table = self.model_table[self.model_table['id'].isin(filtered_idx)]

    def predict(self):
        combined_df = pd.concat([self.model_table, self.user_df], ignore_index=True)
        # "genre" 열의 장르들을 숫자로 매핑
        vectorizer = CountVectorizer(tokenizer=lambda x: x.split(', '))
        genre_matrix = vectorizer.fit_transform(combined_df['genre'])
        genre_df = pd.DataFrame(genre_matrix.toarray())
    
        # tag 데이터와 genre 데이터 결합
        if self.tag == -1:
            tag_df = combined_df.drop(['id', 'genre'], axis=1)
            df_final = pd.concat([tag_df, genre_df], axis=1)
        else: df_final = genre_df
        
        # 코사인 유사도 계산
        similarity_matrix = cosine_similarity(df_final)

        # 유사도 행렬을 데이터프레임으로 변환
        similarity_df = pd.DataFrame(similarity_matrix, index=df_final.index, columns=df_final.index)
        
        # 상위 5개 유사한 항목 찾기
        item_id = 0  # 기준 항목의 인덱스
        similar_items = similarity_df[item_id].nlargest(len(self.user_df) + 5)[len(self.user_df):]  # 상위 5개 유사한 항목 (자기 자신 제외)
        similar_item_ids = similar_items.index.tolist()

        # 추천 게임 목록 생성
        recommendations = combined_df.loc[similar_item_ids, 'id'].tolist()

        return recommendations
    

class EASEModel():
    def __init__(self, age, platform, players, major_genre, tag, user_games_names):
        self.user_games_names = list(user_games_names)
        self.age = age
        self.platform = platform
        self.players = players
        self.major_genre = major_genre
        self.tag = tag

        self.load_game_data()
        self.preprocess()
        
    def load_game_data(self):
        #engine = create_engine(POSTGRE)
        load_dotenv()
        engine = create_engine(f"postgresql://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_DATABASE']}")
        self.game_table = pd.read_sql_table(table_name="game", con=engine)
        self.model_table = pd.read_sql_table(table_name="Ease", con=engine)
        
        train_set = pd.read_sql_table(table_name="user_train", con=engine)
        test_set = pd.read_sql_table(table_name="user_test", con=engine)
        self.user_table = pd.concat([train_set, test_set])
        self.user_table = self.user_table.sort_values(by='user_idx') 

    def preprocess(self):
        # input preprocess
        self.game_id = []
        for i in self.user_games_names:
            input_idx = self.game_table[self.game_table['name'] == i]
            self.game_id.append(input_idx['id'].values[0])

        # model_table preprocess
        # user_idx로 묶어서 id를 배열로 합치기
        self.user_table = self.user_table.groupby('user_idx')['id'].apply(list).reset_index()
        self.user_table["id"] = self.user_table["id"].apply(lambda x: np.array(x, dtype=int))
    
    def predict(self):
        def game_similarity(arr1, arr2):
            set1 = set(arr1)
            set2 = set(arr2)

            intersection = set1.intersection(set2)
            similarity = len(intersection)

            return similarity
        
        def select_similar_user_idx(df):
            if len(df) <= 3:
                return list(df['user_idx'])
            else:
                return random.sample(list(df['user_idx']), 3)
        
        self.user_table['similarity'] = self.user_table['id'].apply(lambda x: game_similarity(x, self.game_id))
        
        similarity_df = self.user_table[self.user_table['similarity'] == max(self.user_table['similarity'])]
        similarity_df_ = self.model_table[self.model_table['user'].isin(select_similar_user_idx(similarity_df))]
        
        df_extracted = self.game_table[self.game_table['id'].isin(list(similarity_df_['item']))]
        df_extracted = df_extracted.set_index('id')
        df_extracted = df_extracted.loc[list(similarity_df_['item'])]
        df_extracted = df_extracted.reset_index()

        final_id = filter(df_extracted, self.age, self.platform, self.players, self.major_genre, 'cf')
        return list(final_id)

        

