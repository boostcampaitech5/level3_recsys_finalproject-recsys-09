import os

from loguru import logger

from core.errors import PredictException, ModelLoadException
from core.config import MODEL_NAME, MODEL_PATH, POSTGRE, API_KEY

# model
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# data
from sqlalchemy import create_engine
import pandas as pd
from services.filters import filter

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

class ContentBaseModel():
    def __init__(self, user_data):
        self.user_games_names = user_data.games
        self.age = int(user_data.age)
        self.platform = user_data.platform
        self.players = int(user_data.players)
        self.major_genre = user_data.major_genre
        self.tag = self.tag_preprocessing(user_data.tag)

        self.load_game_data()
        self.preprocess_input()
        self.filtering_data()
    
    def tag_preprocessing(self, tags):
        tag_list = ['Graphics', 'Sound', 'Creativity', 'Freedom', 'Hitting', 'Completion', 'hard']
        user_tag = []
        for i in tag_list:
            if i in tags:
                user_tag.append(1)
            else:
                user_tag.append(0)
        return user_tag

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
        recommendations = combined_df.loc[similar_item_ids, 'id'].tolist()

        return recommendations


def chatGPT(user_data):
    # set api key
    openai.api_key = API_KEY 

    message = "{}살이상이고 {}를 가지고 있고 {}인 게임을 선호해. 해본 게임은 {}야".format(user_data.age, user_data.platform, user_data.players, user_data.games)

    # Call the chat GPT API
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"게임을 플레이한 유저의 정보를 보여줄테니까 이 정보를 바탕으로 게임 5개를 이름만 추천해줘"},
            {"role": "system", "content": f"게임의 정식 명칭으로 추천 해주고 유저가 이미 플레이 한 게임은 추천하지 말아줘."},
            {"role": "assistant", "content": f"다음 예시와 같이 대답해줘. 1. 게임1 2. 게임2 3. 게임3 4. 게임4 5. 게임5"},
            {"role": "user", "content": message}
        ],
        temperature=0,
        max_tokens=100
    )
    return completion['choices'][0]['message']['content']