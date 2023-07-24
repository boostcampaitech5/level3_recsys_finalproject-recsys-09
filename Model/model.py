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
        self.user_games_names = [x for x in self.user_games_names if x != '']
        if not self.user_games_names:
            return
        
        if self.tag == -1:
            columns=['id', 'genre']
        else:
            columns = ['id', 'genre', 'graphics', 'sound', 'creativity', 'freedom', 'hitting', 'completion', 'difficulty']
        self.user_df = pd.DataFrame(columns=columns)

        for i in self.user_games_names:
            input_idx = list(self.game_table[self.game_table['name'] == i]['id'])
            input_df =  self.model_table[self.model_table['id'].isin(input_idx)]
            self.user_df = pd.concat([self.user_df, input_df[['id', 'genre']]], ignore_index=True)
            if not self.user_df.empty:
                return 
        if self.tag != -1:
            self.user_df = self.user_df.fillna(dict(zip(self.user_df.columns[2:], self.tag)))

    def filtering_data(self):
        filtered_idx = filter(self.game_table, self.age, self.platform, self.players, self.major_genre, 'cb')
        self.model_table = self.model_table[self.model_table['id'].isin(filtered_idx)]

    def predict(self):
        if not self.user_games_names:
            return []
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
        self.flag=0

        self.load_game_data()
        self.preprocess()
        
    def load_game_data(self):
        #engine = create_engine(POSTGRE)
        load_dotenv()
        engine = create_engine(f"postgresql://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_DATABASE']}")
        self.game_table = pd.read_sql_table(table_name="game", con=engine)
        self.model_table = pd.read_sql_table(table_name="Ease", con=engine)
        self.user_table = pd.read_sql_table(table_name="cf_model", con=engine)

    def preprocess(self):
        # input preprocess
        self.game_id = []
        self.user_games_names = [x for x in self.user_games_names if x != '']
        if not self.user_games_names:
            return
        
        for i in self.user_games_names:
            input_idx = self.game_table[self.game_table['name'] == i]
            if not input_idx.empty:
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
        
        if not self.game_id:
            return []
        
        self.user_table['similarity'] = self.user_table['id'].apply(lambda x: game_similarity(x, self.game_id))
        
        similarity_df = self.user_table[self.user_table['similarity'] == max(self.user_table['similarity'])]
        similarity_df_ = self.model_table[self.model_table['user'].isin(select_similar_user_idx(similarity_df))]
        
        df_extracted = self.game_table[self.game_table['id'].isin(list(similarity_df_['item']))]
        df_extracted = df_extracted.set_index('id')
        df_extracted = df_extracted.loc[list(similarity_df_['item'])]
        df_extracted = df_extracted.reset_index()

        final_id = filter(df_extracted, self.age, self.platform, self.players, self.major_genre, 'cf')
        return list(final_id)

        
class HybridModel():
    def __init__(self, age, platform, players, major_genre, tag, user_games_id):
        self.user_games_id = list(user_games_id)
        self.age = age
        self.platform = platform
        self.players = players
        self.major_genre = major_genre
        self.tag = -1 if tag[0] == -1 else tag # tag 상관없음 처리

        if self.user_games_id:
            self.load_game_data()
            self.preprocess()
        
    def load_game_data(self):
        #engine = create_engine(POSTGRE)
        load_dotenv()
        engine = create_engine(f"postgresql://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_DATABASE']}")
        self.game_table = pd.read_sql_table(table_name="game", con=engine)
        self.model_table = pd.read_sql_table(table_name="Ease", con=engine)
        self.cf_table = pd.read_sql_table(table_name="cf_model", con=engine)
        self.cb_table = pd.read_sql_table(table_name="cb_model", con=engine)
        
    def preprocess(self):
        # model_table preprocess
        # user_idx로 묶어서 id를 배열로 합치기
        self.cf_table = self.cf_table.groupby('user_idx')['id'].apply(list).reset_index()
        self.cf_table["id"] = self.cf_table["id"].apply(lambda x: np.array(x, dtype=int))

        # user game log preprocess
        if self.tag == -1:
            columns=['id', 'genre']
        else:
            columns = ['id', 'genre', 'graphics', 'sound', 'creativity', 'freedom', 'hitting', 'completion', 'difficulty']
        self.df_user = pd.DataFrame(columns=columns)

        for i in self.user_games_id:
            input_df =  self.cb_table[self.cb_table['id']== i]
            self.df_user = pd.concat([self.df_user, input_df[['id', 'genre']]], ignore_index=True)
        if self.tag != -1:
            self.df_user = self.df_user.fillna(dict(zip(self.df_user.columns[2:], self.tag)))

    def cf_predict(self):
        def game_similarity(arr1, arr2):
            set1 = set(arr1)
            set2 = set(arr2)

            intersection = set1.intersection(set2)
            similarity = len(intersection)

            return similarity
        
        def select_similar_user(df):
            if len(df) > 3:
                df['id'] = df['id'].apply(lambda x: x[:5])
            return df
        
        self.cf_table['similarity'] = self.cf_table['id'].apply(lambda x: game_similarity(x, self.user_games_id))

        similarity_df = self.cf_table[self.cf_table['similarity'] == max(self.cf_table['similarity'])]
        similarity_df = select_similar_user(similarity_df)

        ease_predict = self.model_table[self.model_table['user'].isin(list(similarity_df['user_idx']))]

        self.combined_ids = similarity_df['id'].explode().tolist()
        self.combined_ids = self.combined_ids + list(ease_predict['item'])

    def cb_predict(self):
        # 사전에 입력받은 유저정보로 필터링
        idx = filter(self.game_table, self.age, self.platform, self.players, self.major_genre, 'cb')
        filtered_df = self.cb_table[self.cb_table['id'].isin(self.combined_ids)]
        filtered_df = filtered_df[filtered_df['id'].isin(idx)]

        # 유사도 계산 시작 
        self.final_df = pd.concat([filtered_df, self.df_user], ignore_index=True)

        # 'id' 중복 제거, 중복이 있다면 뒤에 것을 남김
        self.final_df = self.final_df.drop_duplicates(subset='id', keep='last')

        # "genre" 열의 장르들을 숫자로 매핑
        vectorizer = CountVectorizer(tokenizer=lambda x: x.split(', '))
        genre_matrix = vectorizer.fit_transform(self.final_df['genre'])
        genre_df = pd.DataFrame(genre_matrix.toarray())

        # "id" 열 제외
        df_numeric = self.final_df.drop(['id', 'genre'], axis=1)

        # 숫자 데이터와 장르 데이터 결합
        df_combined = pd.concat([df_numeric, genre_df], axis=1)

        # 코사인 유사도 계산
        similarity_matrix = cosine_similarity(df_combined)

        # 유사도 행렬을 데이터프레임으로 변환
        similarity_df = pd.DataFrame(similarity_matrix, index=self.final_df.index, columns=self.final_df.index)

        # 상위 5개 유사한 항목 찾기
        item_id = 0  # 기준 항목의 인덱스
        similar_items = similarity_df[item_id].nlargest(len(self.df_user) + 5)[len(self.df_user):]  # 상위 5개 유사한 항목 (자기 자신 제외)

        # 상위 5개 유사한 항목의 인덱스
        similar_item_ids = similar_items.index.tolist()

        # 추천 게임 목록 생성
        self.recommendations = self.final_df.loc[similar_item_ids, 'id'].tolist()

    def predict(self):
        if not self.user_games_id:
            return []
        
        self.cf_predict()
        self.cb_predict()

        return self.recommendations