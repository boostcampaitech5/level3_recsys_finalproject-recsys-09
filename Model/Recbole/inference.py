from trainer.rebole_inference import inference, test_inference
import argparse 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='EASE-Jul-17-2023_15-17-12.pth')
    parser.add_argument('--topk', type=int, default=5)
    parser.add_argument('--save_path', type=str, default='submission.csv')
    
    args = parser.parse_args()
    
    # inference(args.path)
    test_inference(args.path,args.topk,args.save_path)
    #game_log = [12833, 12864, 11550]
    #inference(game_log, args.path,args.topk,args.save_path)