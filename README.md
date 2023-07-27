![KakaoTalk_Photo_2023-07-27-14-14-41](https://github.com/boostcampaitech5/level3_recsys_finalproject-recsys-09/assets/44831566/ed5a89e3-a09c-4874-8e4c-a37f91dccd01)
## 1️⃣ Introduction

### 1) Background
주변 친구들이나 유튜브, 인터넷 방송 등의 기존의 추천 방식으로는 개인 취향을 반영한 게임을 찾기 어렵습니다. 기존의 사용자 맞춤 게임 추천 서비스도 한 플랫폼 내에서만 정보를 이용하다 보니 관련도가 떨어지고, 플랫폼별 인기 게임의 특징과 장르 차이로 인해 추천 결과가 상이합니다. 이러한 문제를 해결하기 위해 겜픽이라는 다양한 게임 플랫폼을 아우르는 개인 맞춤 게임 추천 웹 서비스를 개발하게 되었습니다.

### 2) Project Objective
<img margin="Auto" width="600" alt="스크린샷 2023-07-27 오후 1 30 52" src="https://github.com/boostcampaitech5/level3_recsys_finalproject-recsys-09/assets/44831566/a2bce2b7-22c8-4066-8774-d057f568d6a9">

- 다양한 게임 플랫폼을 통합하여 사용자 맞춤 게임 추천을 제공합니다. 사용자는 여러 플랫폼에 접속하지 않고도 한 곳에서 다양한 게임 추천을 받을 수 있어 효율적으로 게임을 찾을 수 있습니다.

- 사용자가 경험했던 모든 게임 기록을 고려하여 취향을 정교하게 반영한 추천 결과를 제공합니다. 이로 인해 사용자에게 맞춤형이고 다양한 게임 추천이 가능합니다.

- 게임별 사용자 리뷰 데이터를 분석하여 게임의 특징을 파악하고, 사용자의 관점에서 진솔하고 직접적인 평가를 반영하여 게임 추천에 도움이 되는 정보를 제공합니다. 이를 통해 사용자는 더욱 신뢰성 있는 추천을 받을 수 있습니다.

---

## 2️⃣ Service Architecture

### 1) Project Tree

```
📦level3_recsys_finalproject-recsys-09
├─ 📂.github
│  ├─ 📂ISSUE_TEMPLATE
│  │  ├─ 📜기능-수정.md
│  │  ├─ 📜버그-발견.md
│  │  └─ 📜새로운-기능-추가.md
│  ├─ 📜PULL_REQUEST_TEMPLATE.md
│  └─ 📂workflows
│     ├─ 📜model_serving.yml
│     └─ 📜web_serving.yml
├─ 📜.gitignore
├─ 📂Backend
│  ├─ 📂backend_model
│  │  ├─ 📜.dockerignore
│  │  ├─ 📜.gitignore
│  │  ├─ 📜.pylintrc
│  │  ├─ 📂app
│  │  │  ├─ 📂api
│  │  │  │  ├─ 📂routes
│  │  │  │  │  ├─ 📜api.py
│  │  │  │  │  ├─ 📜model_hb.py
│  │  │  │  │  ├─ 📜openapi.py
│  │  │  │  │  ├─ 📜popular.py
│  │  │  │  │  └─ 📜__init__.py
│  │  │  │  └─ 📜__init__.py
│  │  │  ├─ 📂core
│  │  │  │  ├─ 📜config.py
│  │  │  │  ├─ 📜errors.py
│  │  │  │  ├─ 📜event.bak
│  │  │  │  ├─ 📜events.py
│  │  │  │  ├─ 📜logging.py
│  │  │  │  ├─ 📜paginator.py
│  │  │  │  └─ 📜__init__.py
│  │  │  ├─ 📜main.py
│  │  │  ├─ 📂models
│  │  │  │  └─ 📜prediction.py
│  │  │  ├─ 📂services
│  │  │  │  ├─ 📜filters.py
│  │  │  │  ├─ 📜predict.py
│  │  │  │  └─ 📜preprocess.py
│  │  │  ├─ 📜test_api.py
│  │  │  └─ 📜__init__.py
│  │  ├─ 📜docker-compose.yml
│  │  ├─ 📜Makefile
│  │  ├─ 📜poetry.lock
│  │  ├─ 📜pyproject.toml
│  │  └─ 📜README.md
│  └─ 📂web
│     ├─ 📜.dockerignore
│     ├─ 📂api
│     │  ├─ 📜abtest_output.py
│     │  ├─ 📜home.py
│     │  ├─ 📜input.py
│     │  └─ 📜output.py
│     ├─ 📜app.py
│     ├─ 📂core
│     │  ├─ 📜config.py
│     │  ├─ 📜input_process.py
│     │  ├─ 📜output_process.py
│     │  ├─ 📜preload.py
│     │  └─ 📜save_db.py
│     ├─ 📂database
│     │  └─ 📜db.py
│     ├─ 📜poetry.lock
│     ├─ 📜pyproject.toml
│     └─ 📂schemas
│        ├─ 📜request.py
│        └─ 📜response.py
├─ 📂Data
│  ├─ 📂bigquery
│  │  └─ 📜big_query.ipynb
│  ├─ 📂crawling
│  │  ├─ 📜game_data_crawling.ipynb
│  │  ├─ 📜game_url_crawling.py
│  │  ├─ 📜GPT_review.ipynb
│  │  ├─ 📜MetaCriticScraper.py
│  │  ├─ 📜review_sample_crawling.ipynb
│  │  └─ 📜user_crawling.ipynb
│  ├─ 📂postgre
│  │  └─ 📜postgre.ipynb
│  └─ 📂preprocess
│     ├─ 📜#_of_player_mapping.ipynb
│     ├─ 📜data_preprocess.ipynb
│     ├─ 📜genre_mapping.ipynb
│     ├─ 📜test_user_sampling.ipynb
│     └─ 📜user_crawling_preprocess.ipynb
├─ 📂Frontend
│  ├─ 📂image
│  │  ├─ 📜favicon.png
│  │  ├─ 📜home_button.png
│  │  ├─ 📜logo.png
│  │  ├─ 📜spin.gif
│  │  ├─ 📜start_button.png
│  │  ├─ 📜submit_button.png
│  │  └─ 📜survey_button.png
│  ├─ 📜input.css
│  ├─ 📜input.html
│  ├─ 📜input.js
│  ├─ 📜main.css
│  ├─ 📜main.html
│  ├─ 📜next.js
│  ├─ 📜output.css
│  ├─ 📜output.html
│  └─ 📜search.js
├─ 📂Model
│  ├─ 📜model.py
│  ├─ 📜performance_check.py
│  ├─ 📂Recbole
│  │  ├─ 📜inference.py
│  │  ├─ 📜main.py
│  │  ├─ 📜preprocess.py
│  │  ├─ 📜requirements.txt
│  │  ├─ 📂trainer
│  │  │  ├─ 📜rebole_inference.py
│  │  │  └─ 📜rebole_train.py
│  │  └─ 📂utils
│  │     └─ 📜preprocess_data.py
│  └─ 📂src
│     ├─ 📜filters.py
│     └─ 📜precision_recall.py
└─ 📜README.md
```

### 2) Service Overview
<img width="1067" alt="스크린샷 2023-07-27 오후 3 35 48" 
src="https://github.com/boostcampaitech5/level3_recsys_finalproject-recsys-09/assets/44831566/c2426a14-43b0-40d1-99ba-d536cf26dadd">

1. 웹 서비스가 시작되면 웹 페이지에 시작 화면이 전시됩니다.
2. 사용자는 서비스의 [START] 버튼을 클릭하면 사용자 정보 입력 페이지로 이동합니다.
3. 사용자는 나이, 선호 장르, 보유중인 게임 장비, 해봤던 게임 등 사용자 정보를 입력합니다.
4. 해당 정보는 FastAPI를 통해 Modeling Component에 전달됩니다.
5. Modeling 모듈에서는 사용자 정보 전처리 → 기존 유저와의 유사도 분석 → 새로운 유저의 추천 목록 생성 → 사용자 정보를 통한 필터링을 수행합니다.
6. 필터링된 추천 아이템 목록은 FastAPI를 통해 웹 서비스로 전송됩니다.
7. 서비스는 데이터 저장소로부터 추천 아이템 ID 목록에 해당하는 URL과 제품 image, 장르 정보를 추출하여 웹 페이지에 전시합니다.

---

## 3️⃣ DataSet

### 1) 데이터셋 수집

- 1차 : Metacritic 사이트의 games this year (2000년 ~ 2023년) 데이터 크롤링
    - https://www.metacritic.com/browse/games/score/metascore/year/all/filtered
- 2차 : 1차배포의 피드백을 통한 부족한 게임들을 직접 DB에 추가

### 2) Database ERD
<img width="800" alt="스크린샷 2023-07-27 오후 4 00 20" src="https://github.com/boostcampaitech5/level3_recsys_finalproject-recsys-09/assets/44831566/232416e2-2d38-4e53-a99f-4d6019f050eb">

- 게임 이름을 id로 나타내는 column을 전체 테이블의 Primary Key로 설정
- Game table에 앞서 메타 크리틱을 통해 수집한 게임들의 데이터를 저장
- CB 모델 table에는 GPT 모델을 이용하여 구한 게임 태그 데이터가 포함되며 이는 content based model로 제품을 추천할 때 사용
- 각 게임에 리뷰를 남긴 유저들의 리뷰 게임 목록을 수집하여 각 유저들과 게임 이름을 인덱스화 하여 각각 cf_model 테이블, user 테이블에 저장
- 당장의 구현 과정에서는 사용하지 않지만 추후 서비스 고도화에 사용할 수 있는 정보들은 따로 details 테이블에 저장


---

## 4️⃣ Modeling

### 1) Flow Chart

![그림4](https://github.com/boostcampaitech5/level3_recsys_finalproject-recsys-09/assets/44831566/926135c3-4c32-454d-a68b-a00bd9c27481)

![그림5](https://github.com/boostcampaitech5/level3_recsys_finalproject-recsys-09/assets/44831566/1081a0b3-5e93-4603-9fca-9caa0ff37cfa)


### 2) Model Train

- 

### 2) Preprocessing

- 배경 제거 Segmentation을 위해 UNet 기반 rembg 적용
- 3 x 224 x 224 image resizing
- Data normalization

### 3) Feature Extraction

- ResNet34의 convolution part 적용
- 3 x 224 x 224 크기의 image로부터 1 x 512 크기의 feature vector 추출

### 4) Multi-Classification

- 512-512-13 구조의 Multi layer perceptron 적용
- Test dataset 기준 accuracy 78.12%

### 5) Top-K Recommender

- 저장된 feature data들과 cosine similarity를 계산하여 Top-K 이미지 선택

---

## 5️⃣Product Serving

### 1) SW 구성

![https://user-images.githubusercontent.com/91198452/172394318-980681d3-cb23-44db-af1b-63d94f8869fb.png](https://user-images.githubusercontent.com/91198452/172394318-980681d3-cb23-44db-af1b-63d94f8869fb.png)

### 2) FrontEnd (Streamlit)

- 사용자 인터페이스 제공 : 이미지 업로드, 크롭, 전시 등
- 서비스 결과 전시 : 제품 유형, 유사 제품 이미지, 제품 링크, 가격 등

### 3) BackEnd (FastAPI)

- Model 과 FrontEnd 를 연결
- Client로부터 데이터를 수신하여 Inference 모듈을 호출
- Inference 모듈로부터 추론 결과를 수신하여 Client로 전송

### 4) Docker

- FrontEnd와 BackEnd가 각각 독립된 Docker container 상에서 실행
- Docker-compose를 이용해 즉시 실행 가능

---

## 6️⃣ **How to Run**

You need install [Docker](https://www.docker.com/) first

### run

```
docker-compose build
docker-compose up
```

### delete container

```
docker-compose down
```

### without docker

```
cd Backend/
python main.py

cd ../Frontend
streamlit run demo.py
```

## 7️⃣ **Demo (시연 영상)**

- 시연영상

![시연영상](https://user-images.githubusercontent.com/78737997/173265924-5563255e-480d-467b-a2df-5383cf8586ac.gif)

## 8️⃣ Reference

- [https://www.kaggle.com/code/hamditarek/similar-image-cnn-cosine-similarity](https://www.kaggle.com/code/hamditarek/similar-image-cnn-cosine-similarity)

## 9️⃣ 팀원 소개

| 이름 | GitHub | 역할 |
| — | — | — |
| 강영석 | [kysuk05](https://github.com/kysuk05)  | 프론트엔드(streamlit), GitHub, 백엔드 |
| 김수희 | [Kimsuhhee](https://github.com/Kimsuhhee) | 데이터베이스, 크롤링, 전처리  |
| 김예지 | [imyjk729](https://github.com/imyjk729) | 전처리, 특징추출, Top-K 추천 |
| 이현우 | [harrier999](https://github.com/harrier999)  | 백엔드(FastAPI), Docker, 크롤링 |
| 홍수연 | [sparklingade](https://github.com/sparklingade)  | PM, 전처리, 크롤링 |
