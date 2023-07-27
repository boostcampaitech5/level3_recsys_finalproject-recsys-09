# model
import openai
# data
import numpy as np
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
        self.model_table = load_data_from_redis('Ease')
        self.user_table = load_data_from_redis('cf_model')
    
    def preprocess(self):
        # model_table preprocess
        # user_idx로 묶어서 id를 배열로 합치기
        self.user_table = self.user_table.groupby('user_idx')['id'].apply(list).reset_index()
        self.user_table["id"] = self.user_table["id"].apply(lambda x: np.array(x, dtype=int))
        
    def predict(self):
        if not self.user_games_id:
            return []
        
        self.user_table['similarity'] = self.user_table['id'].apply(lambda x: game_similarity(x, self.user_games_id))

        similarity_df = self.user_table[self.user_table['similarity'] == max(self.user_table['similarity'])]
        similarity_df = self.model_table[self.model_table['user'].isin(select_similar_user_idx(similarity_df))]

        df_extracted = self.game_table[self.game_table['id'].isin(list(similarity_df['item']))]
        df_extracted = df_extracted.set_index('id')
        df_extracted = df_extracted.loc[list(similarity_df['item'])]
        df_extracted = df_extracted.reset_index()

        final_id = filter(df_extracted, self.age, self.platform, self.players, self.major_genre, 'cf')
        return list(final_id)[:10]
    

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
        self.idx = filter(self.game_table, self.age, self.platform, self.players, self.major_genre, 'cb')

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