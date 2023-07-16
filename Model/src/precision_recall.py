def compute_precision_recall(targets, predictions, k=5):
    """
		targets : 테스트 데이터 중, 사용자의 피드백이 있는 item 인덱스 리스트
		predictions : 학습 데이터에 피드백이 존재하는 item을 제외한 예측 데이터
		k : 추천 수
    """
    pred = predictions[:k]
    num_hit = len(set(pred).intersection(set(targets)))
    precision = float(num_hit) / len(pred)
    recall = float(num_hit) / len(targets)
    return precision, recall