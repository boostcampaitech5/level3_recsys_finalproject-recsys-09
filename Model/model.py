# model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from MetaCriticScraper import MetaCriticScraper
# data
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

class ContentBaseModel():
    def __init__(self, user_games_names):
        self.user_games_names = user_games_names
        self.load_game_data()

    def load_game_data(self):
        load_dotenv()
        engine = create_engine(f"postgresql://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_DATABASE']}")
        game_table = "game"
        self.game_table = pd.read_sql_table(table_name=game_table, con=engine)

    def preprocess_input(self):
        self.user_df = pd.DataFrame(columns=['id', 'name', 'genre'])
        for i in self.user_games_names:
            tmp = self.game_table[self.game_table['name'] == i]
            self.user_df = pd.concat([self.user_df, tmp[['id', 'name', 'genre']]], ignore_index=True)

    def predict(self):
        db_df = self.game_table[['name', 'genre']]

        # 기존 게임 데이터프레임과 유저 게임 데이터프레임 통합
        combined_df = pd.concat([db_df, self.user_df], ignore_index=True)

        conbined_df = conbined_df.drop_duplicates(subset=['name'], keep='last')

        # TF-IDF 벡터화 객체 생성
        vectorizer = TfidfVectorizer()

        # 게임 장르 데이터를 TF-IDF 벡터로 변환
        genre_vectors = vectorizer.fit_transform(combined_df['genre'])

        # 추천을 위한 유사도 측정
        similarities = cosine_similarity(genre_vectors[-len(self.user_games_names):], genre_vectors[:-len(self.user_games_names)])
        top_similar_indices = similarities.argsort()[0][::-1][:5] #5개 추천

        # 추천 게임 목록 생성
        recommendations = combined_df.loc[top_similar_indices, 'id'].tolist()


        return recommendations
    
    


