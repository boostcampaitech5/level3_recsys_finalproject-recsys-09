import numpy as np
import torch
from tqdm import tqdm
from recbole.quick_start.quick_start import load_data_and_model
from recbole.utils.case_study import full_sort_topk, full_sort_scores
import pandas as pd
import os
import concurrent.futures
"""from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
engine = create_engine(f"postgresql://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_DATABASE']}")"""

def inference(game_log, model_path='EASE-Jun-10-2023_14-11-23.pth', topk=5, save_path='submission.csv'):
    config, model, dataset, train_data, valid_data, test_data = load_data_and_model(
        model_file=os.path.join('saved',model_path))
    
    del train_data, valid_data
    data = {'user': [-1] * len(game_log),
        'item': game_log}
    df = pd.DataFrame(data)


    print(df)
    user_grp = dict(df.groupby('user').item.apply(list))

    submission = pd.DataFrame({'user': [-1, -1, -1, -1, -1],
                               'item': [-1, -1, -1, -1, -1]})
    sub_user_idx = submission['user'].unique()
    sub_user_idx = np.array(sub_user_idx,dtype=str)
    uid_series = dataset.token2id(dataset.uid_field, sub_user_idx)

    total_topk_score, total_topk_iid_list = torch.zeros_like(torch.Tensor(1, topk)), torch.zeros_like(torch.Tensor(1, topk))

    for idx in tqdm(range(0,len(uid_series))):
        need_inf = dataset.token2id(dataset.iid_field, np.array(user_grp[int(sub_user_idx[idx])],dtype=str))
        mask = [True if i in need_inf else False for i in range(0,6808)]
        scores = full_sort_scores(np.array([uid_series[idx]]),model,test_data,config['device'])
        new_scores=scores.cpu().masked_fill(torch.from_numpy(np.array(mask)),float('-inf'))    
        total_topk_score[idx] = torch.topk(new_scores,topk)[0]
        total_topk_iid_list[idx] = torch.topk(new_scores,topk)[1]
        
    int_iid = total_topk_iid_list.to(torch.int64)
    external_item_list = dataset.id2token(dataset.iid_field, int_iid.cpu())
    external_item_list = external_item_list.flatten()

    print(external_item_list)
    return external_item_list
    
    """config, model, dataset, train_data, valid_data, test_data = load_data_and_model(
        model_file=os.path.join('saved',model_path))
    
    del train_data, valid_data
    
    #submission = pd.read_csv('/opt/ml/input/data/sample_submission.csv')
    submission = {'user': [10000000, 10000000, 10000000, 10000000, 10000000],
                  'item': [-1, -1, -1, -1, -1]}
    sub_user_idx = submission['user'].unique()
    sub_user_idx = np.array(sub_user_idx,dtype=str)
    uid_series = dataset.token2id(dataset.uid_field, sub_user_idx)
    total_topk_score, total_topk_iid_list = torch.zeros_like(torch.Tensor(1, 5)), torch.zeros_like(torch.Tensor(1, 5))
    
    for idx in tqdm(range(0,len(uid_series))):
        topk_score, topk_iid_list = full_sort_topk(np.array([uid_series[idx]]),model,test_data,5,config['device'])
        total_topk_score[idx] = topk_score
        total_topk_iid_list[idx] = topk_iid_list
        
    int_iid = total_topk_iid_list.to(torch.int64)
    external_item_list = dataset.id2token(dataset.iid_field, int_iid.cpu())
    external_item_list = external_item_list.flatten()
    #df = pd.DataFrame({'user': np.repeat(sub_user_idx, 5), 'item': external_item_list})
    #df.to_csv("submission.csv",index=False)
    print(external_item_list)
    return external_item_list"""
    
def test_inference(model_path='EASE-Jun-10-2023_14-11-23.pth',topk=5,save_path='submission.csv'):
    config, model, dataset, train_data, valid_data, test_data = load_data_and_model(
        model_file=os.path.join('saved',model_path))
    
    del train_data, valid_data
    df = pd.read_csv('/opt/ml/input/data/train_set.csv')
    #df = pd.read_sql_table(table_name="user_train", con=engine)
    df = df.rename(columns={'user_idx': 'user', 'id': 'item'})
    user_grp = dict(df.groupby('user').item.apply(list))

    submission = pd.read_csv('/opt/ml/input/data/sample_submission.csv')
    sub_user_idx = submission['user'].unique()
    sub_user_idx = np.array(sub_user_idx,dtype=str)
    uid_series = dataset.token2id(dataset.uid_field, sub_user_idx)
    #total_topk_score, total_topk_iid_list = torch.zeros_like(torch.Tensor(31360, topk)), torch.zeros_like(torch.Tensor(31360, topk))
    total_topk_score, total_topk_iid_list = torch.zeros_like(torch.Tensor(39366, topk)), torch.zeros_like(torch.Tensor(39366, topk))

    for idx in tqdm(range(0,len(uid_series))):
        need_inf = dataset.token2id(dataset.iid_field, np.array(user_grp[int(sub_user_idx[idx])],dtype=str))
        mask = [True if i in need_inf else False for i in range(0,8818)]
        scores = full_sort_scores(np.array([uid_series[idx]]),model,test_data,config['device'])
        new_scores=scores.cpu().masked_fill(torch.from_numpy(np.array(mask)),float('-inf'))    
        total_topk_score[idx] = torch.topk(new_scores,topk)[0]
        total_topk_iid_list[idx] = torch.topk(new_scores,topk)[1]
        
    int_iid = total_topk_iid_list.to(torch.int64)
    external_item_list = dataset.id2token(dataset.iid_field, int_iid.cpu())
    external_item_list = external_item_list.flatten()

    df = pd.DataFrame({'user': np.repeat(sub_user_idx, topk), 'item': external_item_list})
    df.to_csv(save_path,index=False)