# model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# data
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
from filters import filter

class ContentBaseModel():
    def __init__(self, age, platform, players, major_genre, tag, user_games_names):
        self.user_games_names = list(user_games_names)
        self.age = age
        self.platform = platform
        self.players = self.players
        self.major_genre = major_genre
        self.tag = tag

        self.load_game_data()
        self.preprocess_input()
        self.filtering_data()
        

    def load_game_data(self):
        engine = create_engine(POSTGRE)
        game_table = "game"
        self.game_table = pd.read_sql_table(table_name=game_table, con=engine)

    def filtering_data(self):
        self.game_table = filter (self.game_table, self.age, self.platform, self.players, self.major_genre)
    
    def preprocess_input(self):
        print("-----------------------------------------------------------------------------")
        self.user_df = pd.DataFrame(columns=['id', 'name', 'genre'])
        for i in self.user_games_names:
            tmp = self.game_table[self.game_table['name'] == i]
            self.user_df = pd.concat([self.user_df, tmp[['id', 'name', 'genre']]], ignore_index=True)

    def predict(self):
        db_df = self.game_table[['id', 'name', 'genre']]

        print(db_df)

        # 기존 게임 데이터프레임과 유저 게임 데이터프레임 통합
        combined_df = pd.concat([db_df, self.user_df], ignore_index=True)

        combined_df = combined_df.drop_duplicates(subset=['name'], keep='last')

        # print(combined_df)

        # TF-IDF 벡터화 객체 생성
        vectorizer = TfidfVectorizer()

        # 게임 장르 데이터를 TF-IDF 벡터로 변환
        genre_vectors = vectorizer.fit_transform(combined_df['genre'])

        # 추천을 위한 유사도 측정
        similarities = cosine_similarity(genre_vectors[-2:], genre_vectors[:-2])
        top_similar_indices = similarities.argsort()[0][::-1][:5] #5개 추천

        # 추천 게임 목록 생성
        recommendations = combined_df.loc[top_similar_indices, 'id'].tolist()


        return recommendations

