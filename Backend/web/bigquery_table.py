import glob
from google.cloud import bigquery
from google.oauth2 import service_account

# 서비스 계정 키 JSON 파일 경로
key_path = glob.glob("./*.json")[0]

# Credentials 객체 생성
credentials = service_account.Credentials.from_service_account_file(key_path)

# GCP 클라이언트 객체 생성
client = bigquery.Client(credentials = credentials, 
                         project = credentials.project_id)


sql1 = """
CREATE TABLE review.user_info (
    id STRING,
    age INT64,
    platform ARRAY<STRING>,
    players INT64,
    major_genre ARRAY<STRING>,
    tag ARRAY<STRING>,
    games ARRAY<STRING>
);
"""
client.query(sql1).result()

sql2 = """
CREATE TABLE review.gpt_output (
    id STRING,
    games ARRAY<STRING>
);
"""
client.query(sql2).result()

sql3 = """
CREATE TABLE review.hb_output (
    id STRING,
    games ARRAY<INT64>
);
"""
client.query(sql3).result()

sql4 = """
CREATE TABLE review.feedback (
    id STRING,
    likes ARRAY<INT64>
);
"""
client.query(sql4).result()