from trainer.rebole_inference import inference, test_inference
import argparse 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='EASE-Jun-10-2023_14-11-23.pth')
    parser.add_argument('--topk', type=int, default=10)
    parser.add_argument('--save_path', type=str, default='submission.csv')
    
    args = parser.parse_args()
    
    # inference(args.path)
    test_inference(args.path,args.topk,args.save_path)