import pandas as pd
import numpy as np
import os
import glob
from src.precision_recall import compute_precision_recall
import time
from tqdm import tqdm

# 사용자로부터 파일명 입력 받기
folder_path = 'output/'  # 폴더 경로
file_pattern = '*.csv'  # 가져올 파일 패턴
file_list = glob.glob(os.path.join(folder_path, file_pattern))

# 가져온 파일명 출력
for i, file in enumerate(file_list):
    print(f'{i+1}. {file}')

# 사용자에게 선택 받기
selected_index = int(input('선택할 파일 번호를 입력하세요: ')) - 1

# 선택된 파일명 출력
filename = file_list[selected_index]
predict = pd.read_csv(filename)

test_set = pd.read_csv('output/test_set.csv')   #-> 이부분은 db 올라가면 변경

# 컬럼명을 'user', 'item'로 변경
test_set.columns = ['user', 'item']
predict.columns = ['user', 'item']


user_idx = test_set['user'].unique()
precision_list = []
recall_list = []

print('Precision@5 & Recall@5 계산중...')

for i in tqdm(user_idx):
    time.sleep(0.1)
    targets = np.array(test_set[test_set['user'] == i]['item'])
    predictions = np.array(predict[predict['user'] == i]['item'])
    precision, recall = compute_precision_recall(targets, predictions, k=5)

    precision_list.append(precision)
    recall_list.append(recall)

# 결과 출력
print(f'precision@5: {np.mean(precision_list)}')
print(f'   recall@5: {np.mean(recall_list)}')