import os

from loguru import logger

from core.errors import PredictException, ModelLoadException
from core.config import MODEL_NAME, MODEL_PATH, POSTGRE, API_KEY

import openai


class MachineLearningModelHandlerScore(object):
    model = None

    @classmethod
    def predict(cls, input, load_wrapper=None, method="predict"):
        clf = cls.get_model(load_wrapper)
        if hasattr(clf, method):
            return getattr(clf, method)(input)
        raise PredictException(f"'{method}' attribute is missing")

    @classmethod
    def get_model(cls, load_wrapper):
        if cls.model is None and load_wrapper:
            cls.model = cls.load(load_wrapper)
        return cls.model

    @staticmethod
    def load(load_wrapper):
        model = None
        if MODEL_PATH.endswith("/"):
            path = f"{MODEL_PATH}{MODEL_NAME}"
        else:
            path = f"{MODEL_PATH}/{MODEL_NAME}"
        if not os.path.exists(path):
            message = f"Machine learning model at {path} not exists!"
            logger.error(message)
            raise FileNotFoundError(message)
        model = load_wrapper(path)
        if not model:
            message = f"Model {model} could not load!"
            logger.error(message)
            raise ModelLoadException(message)
        return model

# model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# data
from sqlalchemy import create_engine
import pandas as pd

class ContentBaseModel():
    def __init__(self, user_games_names):
        self.user_games_names = list(user_games_names)
        self.load_game_data()
        self.preprocess_input()

    def load_game_data(self):
        engine = create_engine(POSTGRE)
        game_table = "game"
        self.game_table = pd.read_sql_table(table_name=game_table, con=engine)

    def preprocess_input(self):
        print("-----------------------------------------------------------------------------")
        self.user_df = pd.DataFrame(columns=['id', 'name', 'genre'])
        for i in self.user_games_names:
            print(i)
            tmp = self.game_table[self.game_table['name'] == i]
            print(tmp)
            self.user_df = pd.concat([self.user_df, tmp[['id', 'name', 'genre']]], ignore_index=True)

        # print(self.user_df)
        # print(len(self.user_games_names))

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


def chatGPT(user_data):
    # set api key
    openai.api_key = API_KEY 

    # Call the chat GPT API
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"게임을 플레이한 유저의 정보 딕셔너리 형식으로 보여줄테니까 게임 5개를 설명없이 추천해줘"},
            {"role": "system", "content": f"age는 유저의 나이고 players는 게임 인원수고 platform은 사용 가능한 게임 기기이며 games는 유저가 지금까지 한 게임이야"},
            {"role": "system", "content": f"게임의 정식 명칭으로 추천 해주고 games에 있는 게임은 추천하지 말아줘"},
            {"role": "assistant", "content": f"다음 예시와 같이 대답해줘. Chicory: A Colorful Tale, How to Survive, Fantasy Life, Battlezone, The Cave"},
            {"role": "assistant", "content": f"1. The Witcher 3: Wild Hunt 2. Stardew Valley 3. Hollow Knight 4. Celeste 5. Ori and the Blind Forest"},
            # {"role": "assistant", "content": f"전달받은 리뷰가 없으면 다음 예시로 대답해줘. 독창성: 0, 사운드: 0, 그래픽: 0, 자유도: 0, 타격감: 0, 완성도: 0, 난이도:0"},
            {"role": "user", "content": user_data}
        ],
        temperature=0,
        max_tokens=100
    )
    return completion['choices'][0]['message']['content']