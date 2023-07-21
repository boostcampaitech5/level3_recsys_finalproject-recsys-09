import os 
import pandas as pd 
import numpy as np 
import torch 

from recbole.model.general_recommender.bpr import BPR
from recbole.model.general_recommender.ease import EASE
from recbole.model.general_recommender.lightgcn import LightGCN
from recbole.model.general_recommender.multivae import MultiVAE
from recbole.model.general_recommender.neumf import NeuMF
from recbole.model.general_recommender.admmslim import ADMMSLIM

from recbole.model.context_aware_recommender.ffm import FFM
from recbole.model.context_aware_recommender.fm import FM
from recbole.model.context_aware_recommender.deepfm import DeepFM

from recbole.model.sequential_recommender.gru4rec import GRU4Rec
from recbole.model.sequential_recommender.gru4recf import GRU4RecF
from recbole.model.sequential_recommender.bert4rec import BERT4Rec
from recbole.model.sequential_recommender.sasrec import SASRec



from recbole.config import Config
from recbole.data import create_dataset, data_preparation, Interaction
from recbole.utils import init_logger, get_trainer, get_model, init_seed, set_color
from recbole.quick_start import load_data_and_model, run_recbole
from recbole.utils.case_study import full_sort_topk

from logging import getLogger

def general_train(model_name='ease'):
    logger = getLogger()
    
    if model_name=='lightgcn':
        config = Config(model='LightGCN',dataset='general_train',config_file_list=[f"general_yaml/{model_name}.yaml"])
    
    elif model_name == 'multivae':
        config = Config(model='MultiVAE',dataset='general_train',config_file_list=[f"general_yaml/{model_name}.yaml"])
        
    elif model_name == 'neumf':
        config = Config(model='NeuMF',dataset='general_train',config_file_list=[f"general_yaml/{model_name}.yaml"])
    elif model_name =='admmslim':
        config = Config(model='ADMMSLIM',dataset='general_train',config_file_list=[f"general_yaml/{model_name}.yaml"])
    elif model_name == 'recvae':
        config = Config(model='RecVAE',dataset='general_train',config_file_list=[f"general_yaml/{model_name}.yaml"])
    else:
        config = Config(model=model_name.upper(),dataset='general_train',config_file_list=[f"general_yaml/{model_name}.yaml"])
    
    config['show_progress'] = False 
    config['device'] = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    init_seed(config['seed'], config['reproducibility'])
    init_logger(config)

    logger.info(config)
    
    # dataset filtering
    dataset = create_dataset(config)
    logger.info(dataset)

    # dataset splitting
    train_data, valid_data, test_data = data_preparation(config, dataset)
    
    init_seed(config['seed'], config['reproducibility'])
    if model_name =='ease':
        model = EASE(config, train_data.dataset).to(config['device'])
    elif model_name == 'bpr':
        model = BPR(config, train_data.dataset).to(config['device'])
    elif model_name == 'lightgcn':
        model = LightGCN(config, train_data.dataset).to(config['device'])
    elif model_name == 'multivae':
        model = MultiVAE(config, train_data.dataset).to(config['device'])
    elif model_name == 'neumf':
        model = NeuMF(config, train_data.dataset).to(config['device'])
    elif model_name == 'admmslim':
        model = ADMMSLIM(config, train_data.dataset).to(config['device'])
    elif model_name =='recvae':
        imported_model = get_model('RecVAE')
        model = imported_model(config, train_data.dataset).to(config["device"])
    else:
        raise NotImplementedError(f"model {model_name} not implemented")

    logger.info(model)
    
    # trainer loading and initialization
    trainer = get_trainer(config['MODEL_TYPE'], config['model'])(config, model)

    # model training
    best_valid_score, best_valid_result = trainer.fit(
        train_data, valid_data, saved=True, show_progress=config['show_progress']
    )
    
    test_result = trainer.evaluate(test_data,load_best_model=True,show_progress=config['show_progress'])
    
    print(test_result)

def context_train(model_name='ffm'):
    logger = getLogger()

    if model_name=='ffm':
        config = Config(model='FFM', dataset="context_train", config_file_list=[f'context_yaml/ffm.yaml'])
    elif model_name=='fm':
        config = Config(model='FM', dataset="context_train", config_file_list=[f'context_yaml/fm.yaml'])
    elif model_name =='deepfm':
        config = Config(model='DeepFM', dataset="context_train", config_file_list=[f'context_yaml/deepfm.yaml'])    

    else:
        raise NotImplementedError(f"model {model_name} not implemented")
    
    config['epochs'] = 100
    config['show_progress'] = False
    config['device'] = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    init_seed(config['seed'], config['reproducibility'])
    # logger initialization
    init_logger(config)

    logger.info(config)
    
    # dataset filtering
    dataset = create_dataset(config)
    logger.info(dataset)

    # dataset splitting
    train_data, valid_data, test_data = data_preparation(config, dataset)
    
    # model loading and initialization
    init_seed(config['seed'], config['reproducibility'])
    if model_name=='ffm':
        model = FFM(config, train_data.dataset).to(config['device'])
    elif model_name=='fm':
        model = FM(config, train_data.dataset).to(config['device'])
    elif model_name=='deepfm':
        model = DeepFM(config, train_data.dataset).to(config['device'])
        
    logger.info(model)
    
    # trainer loading and initialization
    trainer = get_trainer(config['MODEL_TYPE'], config['model'])(config, model)

    # model training
    best_valid_score, best_valid_result = trainer.fit(
        train_data, valid_data, saved=True, show_progress=config['show_progress']
    )
    
def sequence_train(model_name='gru4recf'):
    
    logger = getLogger()
    
    if model_name=='gru4recf':
        config = Config(model='GRU4RecF',dataset='general_train',config_file_list=[f"sequence_yaml/{model_name}.yaml"])
    elif model_name=='sasrec':
        config = Config(model='SASRec',dataset='general_train',config_file_list=[f"sequence_yaml/{model_name}.yaml"])
    elif model_name=='gru4rec':
        config = Config(model='GRU4Rec',dataset='general_train',config_file_list=[f"sequence_yaml/{model_name}.yaml"])
    elif model_name =='bert4rec':
        config = Config(model='BERT4Rec',dataset='general_train',config_file_list=[f"sequence_yaml/{model_name}.yaml"])
    
    config['show_progress'] = False 
    config['device'] = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    config['epochs'] = 100 # 30
    
    init_seed(config['seed'], config['reproducibility'])
    init_logger(config)

    logger.info(config)
    
    # dataset filtering
    dataset = create_dataset(config)
    logger.info(dataset)

    # dataset splitting
    train_data, valid_data, test_data = data_preparation(config, dataset)
    
    init_seed(config['seed'], config['reproducibility'])
    if model_name =='gru4recf':
        model = GRU4RecF(config, train_data.dataset).to(config['device'])
    elif model_name == 'sasrec':
        model = SASRec(config, train_data.dataset).to(config['device'])
    elif model_name == 'gru4rec':
        model = GRU4Rec(config, train_data.dataset).to(config['device'])
    elif model_name =='bert4rec':
        model = BERT4Rec(config, train_data.dataset).to(config['device'])
    else:
        raise NotImplementedError(f"model {model_name} not implemented")

    logger.info(model)
    
    # trainer loading and initialization
    trainer = get_trainer(config['MODEL_TYPE'], config['model'])(config, model)

    # model training
    best_valid_score, best_valid_result = trainer.fit(
        train_data, valid_data, saved=True, show_progress=config['show_progress']
    )
    
    test_result = trainer.evaluate(test_data,load_best_model=True,show_progress=config['show_progress'])
    
    print(test_result)