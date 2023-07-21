from trainer.rebole_train import *
from trainer.rebole_inference import inference
from utils.preprocess_data import *
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default='ease')
    parser.add_argument('--model_type', type=str, default='general')
    parser.add_argument('--make_yaml', type=str, default='Yes', help='Yes or No')
    
    args = parser.parse_args()
    
    print(args.model_name)
    print(args.make_yaml)
    print(args.model_type)
    
    if args.model_type=='general':
        if args.make_yaml=='Yes':
            make_general_yaml(args.model_name)
        general_train(args.model_name)
        
    elif args.model_type=='context':
        if args.make_yaml=='Yes':
            make_context_yaml(args.model_name)
        context_train(args.model_name)
        
    elif args.model_type=='sequence':
        if args.make_yaml=='Yes':
            make_sequence_yaml(args.model_name)
        sequence_train(args.model_name)
    