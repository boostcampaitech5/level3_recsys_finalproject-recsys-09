import pandas as pd 
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
engine = create_engine(f"postgresql://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_DATABASE']}")

def make_general_dataset():
    
    df = pd.read_sql_table(table_name="user_train", con=engine)
    df = df.rename(columns={'user_idx': 'user', 'id': 'item'})
    
    df.columns=['user_id:token','item_id:token']
    outpath = f"dataset/general_train"
    
    os.makedirs(outpath, exist_ok=True)
    df.to_csv(os.path.join(outpath,"general_train.inter"),sep='\t',index=False)
    
def make_context_dataset():
    
    train = pd.read_sql_table(table_name="user_train", con=engine)

    side_df1 = pd.read_sql_table(table_name="game", con=engine)
    side_df2 = pd.read_sql_table(table_name="details", con=engine)

    # 컬러명 변경
    train = train.rename(columns={'user_idx': 'user', 'id': 'item'})
    side_df1 = side_df1.rename(columns={'id': 'item'})
    side_df2 = side_df2.rename(columns={'id': 'item'})

    major_genre = side_df1[['item','major_genre']]
    platform = side_df1[['item','platform']]
    publisher = side_df2[['item','publisher']]
    release_date = side_df2[['item','release_date']]
    num_of_player = side_df2[['item','num_of_player']]

    def make_feature_sequence(x):
        x = list(set(x))
        y = ""
        for item in x:
            y += str(item + " ")
        return y.rstrip()
    
    major_genre_seq = major_genre.groupby("item")['major_genre'].apply(make_feature_sequence)
    platform_seq = platform.groupby("item")['platform'].apply(make_feature_sequence)
    publisher_seq = publisher.groupby("item")['publisher'].apply(make_feature_sequence)
    release_date_seq = release_date.groupby("item")['release_date'].apply(make_feature_sequence)
    num_of_player_seq = num_of_player.groupby("item")['num_of_player'].apply(make_feature_sequence)
    
    train_df = pd.merge(train, major_genre_seq, on="item",how='left')
    train_df = pd.merge(train_df, platform_seq, on="item",how='left')
    train_df = pd.merge(train_df, publisher_seq, on="item",how='left')
    train_df = pd.merge(train_df, release_date_seq, on="item",how='left')
    train_df = pd.merge(train_df, num_of_player_seq, on="item",how='left')
    
    train_df = train_df.sort_values('user')
    
    train_data = train_df[['user', 'item']].reset_index(drop=True)
    user_data = train_df[['user']].reset_index(drop=True)
    item_data = train_df[['item', 'major_genre', 'platform', 'publisher', 'release_date', 'num_of_player']].drop_duplicates(subset=['item']).reset_index(drop=True)
    
    train_data.columns=['user_id:token', 'item_id:token']
    user_data.columns=['user_id:token']
    item_data.columns=['item_id:token', 'major_genre:token', 'platform:token_seq', 'publisher:token_seq', 'release_date:token_seq', 'num_of_player:token_seq']
    
    outpath = f"dataset/context_train"

    os.makedirs(outpath, exist_ok=True)

    print("Dump Start")

    # 데이터 파일 저장
    train_data.to_csv(os.path.join(outpath,"context_train.inter"),sep='\t',index=False)
    user_data.to_csv(os.path.join(outpath,"context_train.user"),sep='\t',index=False)
    item_data.to_csv(os.path.join(outpath,"context_train.item"),sep='\t',index=False)
    
    print("Dump Complete")

    
def make_general_yaml(model_name):
    
    yaml_data = """
    USER_ID_FIELD: user_id
    ITEM_ID_FIELD: item_id
    TIME_FIELD: timestamp

    load_col:
        inter: [user_id, item_id, timestamp]
    """
    outpath = f"general_yaml"
    
    os.makedirs(outpath, exist_ok=True)
    with open(os.path.join(outpath,f"{model_name}.yaml"),"w") as f:
        f.write(yaml_data)
        

def make_context_yaml(model_name):
    yaml_data = """
    field_separator: '\t'
    USER_ID_FIELD: user_id
    ITEM_ID_FIELD: item_id
    TIME_FIELD: timestamp

    load_col:
        inter: [user_id, item_id, timestamp]
        user: [user_id]
        item: [item_id, year, genre, writer, director]

    train_neg_sample_args:
        uniform: 10
        
    eval_args:
        split: {'RS': [8, 1, 1]}
        group_by: user
        order: RO
        mode: full
    metrics: ['Recall', 'MRR', 'NDCG', 'Hit', 'Precision', 'MAP']
    topk: 10
    valid_metric: Recall@10
    """
    
    outpath = f"context_yaml"
    
    os.makedirs(outpath, exist_ok=True)
    with open(os.path.join(outpath,f"{model_name}.yaml"),"w") as f:
        f.write(yaml_data)
        
def make_sequence_yaml(model_name):
    
    yaml_data="""
    USER_ID_FIELD: user_id
    ITEM_ID_FIELD: item_id
    TIME_FIELD: timestamp

    load_col:
        inter: [user_id, item_id, timestamp]
        
    train_neg_sample_args: ~
    ITEM_LIST_LENGTH_FIELD: item_length
    LIST_SUFFIX: _list
    MAX_ITEM_LIST_LENGTH: 50
    """
    outpath = f"sequence_yaml"
    
    os.makedirs(outpath, exist_ok=True)
    with open(os.path.join(outpath,f"{model_name}.yaml"),"w") as f:
        f.write(yaml_data)
        