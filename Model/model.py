# model
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# data
import pandas as pd
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

        self.load_game_data()
        self.preprocess_input()
        self.filtering_data()
        

    def load_game_data(self):
        engine = create_engine(POSTGRE)
        self.game_table = pd.read_sql_table(table_name="game", con=engine)
        self.model_table = pd.read_sql_table(table_name="cb_model", con=engine)

    def preprocess_input(self):
        print("-----------------------------------------------------------------------------")
        self.user_df = pd.DataFrame(columns=['id', 'genre', 'graphics', 'sound', 'creativity', 'freedom', 'hitting', 'completion', 'difficulty'])
        
        for i in self.user_games_names:
            input_idx = self.game_table[self.game_table['name'] == i].index
            input_df =  self.model_table.loc[input_idx]
            self.user_df = pd.concat([self.user_df, input_df[['id', 'genre']]], ignore_index=True)
            
        self.user_df = self.user_df.fillna(dict(zip(self.user_df.columns[2:], self.tag)))

    def filtering_data(self):
        filtered_idx = filter(self.game_table, self.age, self.platform, self.players, self.major_genre)
        self.model_table = self.model_table[self.model_table['id'].isin(filtered_idx)]

    def predict(self):
        combined_df = pd.concat([self.model_table, self.user_df], ignore_index=True)
        
        # "genre" 열의 장르들을 숫자로 매핑
        vectorizer = CountVectorizer(tokenizer=lambda x: x.split(', '))
        genre_matrix = vectorizer.fit_transform(combined_df['genre'])
        genre_df = pd.DataFrame(genre_matrix.toarray())
    
        # tag 데이터와 genre 데이터 결합
        tag_df = combined_df.drop(['id', 'genre'], axis=1)
        df_final = pd.concat([tag_df, genre_df], axis=1)
        
        # 코사인 유사도 계산
        similarity_matrix = cosine_similarity(df_final)

        # 유사도 행렬을 데이터프레임으로 변환
        similarity_df = pd.DataFrame(similarity_matrix, index=df_final.index, columns=df_final.index)
        
        # 상위 5개 유사한 항목 찾기
        item_id = 0  # 기준 항목의 인덱스
        similar_items = similarity_df[item_id].nlargest(len(self.user_df) + 5)[len(self.user_df):]  # 상위 5개 유사한 항목 (자기 자신 제외)
        similar_item_ids = similar_items.index.tolist()

        # 추천 게임 목록 생성
        recommendations = df_final.loc[similar_item_ids, 'id'].tolist()

        return recommendations

