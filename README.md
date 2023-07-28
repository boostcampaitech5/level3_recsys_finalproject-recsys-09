<p align="center"><img margin="Auto" width="1200" src="https://github.com/boostcampaitech5/level3_recsys_finalproject-recsys-09/assets/44831566/ed5a89e3-a09c-4874-8e4c-a37f91dccd01"></p>

## 1️⃣ Introduction

### 1) Background
주변 친구들이나 유튜브, 인터넷 방송 등의 기존의 추천 방식으로는 개인 취향을 반영한 게임을 찾기 어렵습니다. 기존의 사용자 맞춤 게임 추천 서비스도 한 플랫폼 내에서만 정보를 이용하다 보니 관련도가 떨어지고, 플랫폼별 인기 게임의 특징과 장르 차이로 인해 추천 결과가 상이합니다. 이러한 문제를 해결하기 위해 겜픽이라는 다양한 게임 플랫폼을 아우르는 개인 맞춤 게임 추천 웹 서비스를 개발하게 되었습니다.

### 2) Project Objective
<p align="center"><img margin="Auto" width="600" src="https://github.com/boostcampaitech5/level3_recsys_finalproject-recsys-09/assets/44831566/a2bce2b7-22c8-4066-8774-d057f568d6a9"></p>

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
│  └─ 📂workflows
│     ├─ 📜model_serving.yml
│     └─ 📜web_serving.yml
├─ 📜.gitignore
├─ 📂Backend
│  ├─ 📂backend_model
│  │  ├─ 📂app
│  │  │  ├─ 📂api/routes
│  │  │  │  ├─ 📜api.py
│  │  │  │  ├─ 📜model_hb.py
│  │  │  │  ├─ 📜openapi.py
│  │  │  │  └─ 📜popular.py
│  │  │  ├─ 📂core
│  │  │  ├─ 📜main.py
│  │  │  ├─ 📂models
│  │  │  │  └─ 📜prediction.py
│  │  │  └─ 📂services
│  │  │     ├─ 📜filters.py
│  │  │     ├─ 📜predict.py
│  │  │     └─ 📜preprocess.py
│  │  ├─ 📜Dockerfile
│  │  └─ 📜Makefile
│  └─ 📂web
│     ├─ 📂api
│     │  ├─ 📜home.py
│     │  ├─ 📜input.py
│     │  └─ 📜output.py
│     ├─ 📂core
│     ├─ 📂database
│     ├─ 📂schemas
│     ├─ 📜app.py
│     └─ 📜Dockerfile
├─ 📂Data
│  ├─ 📂crawling
│  │  ├─ 📜game_data_crawling.ipynb
│  │  ├─ 📜GPT_review.ipynb
│  │  ├─ 📜MetaCriticScraper.py
│  │  └─ 📜user_crawling.ipynb
│  ├─ 📂postgre
│  │  └─ 📜postgre.ipynb
│  └─ 📂preprocess
│     ├─ 📜#_of_player_mapping.ipynb
│     ├─ 📜data_preprocess.ipynb
│     ├─ 📜genre_mapping.ipynb
│     └─ 📜test_user_sampling.ipynb
├─ 📂Frontend
│  ├─ 📂image
│  ├─ 📜input.html
│  ├─ 📜main.html
│  └─ 📜output.html
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
│  └─ 📂src
└─ 📜README.md
```

### 2) Service Overview
<p align="center"><img margin="Auto" width="1067" src="https://github.com/boostcampaitech5/level3_recsys_finalproject-recsys-09/assets/44831566/c2426a14-43b0-40d1-99ba-d536cf26dadd"></p>


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
<p align="center"><img margin="Auto" width="800" src="https://github.com/boostcampaitech5/level3_recsys_finalproject-recsys-09/assets/44831566/232416e2-2d38-4e53-a99f-4d6019f050eb"></p>
- 게임 이름을 id로 나타내는 column을 전체 테이블의 Primary Key로 설정
- Game table에 앞서 메타 크리틱을 통해 수집한 게임들의 데이터를 저장
- CB 모델 table에는 GPT 모델을 이용하여 구한 게임 태그 데이터가 포함되며 이는 content based model로 제품을 추천할 때 사용
- 각 게임에 리뷰를 남긴 유저들의 리뷰 게임 목록을 수집하여 각 유저들과 게임 이름을 인덱스화 하여 각각 cf_model 테이블, user 테이블에 저장
- 당장의 구현 과정에서는 사용하지 않지만 추후 서비스 고도화에 사용할 수 있는 정보들은 따로 details 테이블에 저장
- 사용자 입력을 user_info에 입력에 대한 각 모델별 output을 gpt_output, hb_model_output에 사용자 피드백을 final_feedback에 저장
- 위의 데이터는 예외 상황 파악 및 처리, 모델 학습 및 개선을 위한 데이터 수집을 위해 저장


---

## 4️⃣ Modeling
### 1) Flow Chart
<p align="center"><img margin="Auto" width="900" src="https://github.com/boostcampaitech5/level3_recsys_finalproject-recsys-09/assets/44831566/926135c3-4c32-454d-a68b-a00bd9c27481"></p>
<p align="center"><img margin="Auto" width="900" src="https://github.com/boostcampaitech5/level3_recsys_finalproject-recsys-09/assets/44831566/1081a0b3-5e93-4603-9fca-9caa0ff37cfa"></p>

### 2) Model Selection
<p align="center"><img margin="Auto" width="700" src="https://github.com/boostcampaitech5/level3_recsys_finalproject-recsys-09/assets/44831566/9e238c36-7a90-4ff8-aad6-0187f3dd5685"></p>

- 한정된 시간안에 여러가지 다양한 모델을 실험해보기 위해 Recbole 라이브러를 사용
- 우리가 수집한 유저들의 게임로그 데이터의 sparsity는 99.6%로 매우 높았는데, sparse한 데이터와 cold start problem에 특히 강한 Ease 모델이 단일모델 기준 성능이 가장 좋았음
- 결과적으로, Ease를 베이스라인모델로 정하고, 다양한 모델을 결합한 하이브리드 모델을 구상
   
### 3) Model Train

- 수집한 유저 게임로그 데이터를 8:2 비율로 train-test set으로 split
- train set 으로는 모델을 학습시키고, test set에서는 무작위로 masking을 진행 한 뒤 이를 모델이 예측하는 방식으로 성능평가를 진행
- 성능지표는 precision@5, recall@5를 사용

### 4) Collaborate Filtering
- Ease 모델을 통해 사전 수집된 유저들의 추천 결과를 도출
- 이후 새로운 유저가 들어오면 Collaborative Filtering을 통해 사용자들 간의 유사도를 계산하고, 새로운 유저와 유사한 이전 사용자들을 필터링

### 5) Content Based Filtering
- Collaborative Filtering 을 통해 만들어진 추천리스트를 Content-based Filtering을 사용하여 사용자가 선호할 만한 아이템을 필터링

### 6) GPT-3.5-turbo-Model
<p align="center"><img margin="Auto" width="900" src="https://github.com/boostcampaitech5/level3_recsys_finalproject-recsys-09/assets/44831566/a5e1c3d0-a7c7-46ce-be5a-810a5c7753c9"></p>

- 대화형 인터페이스를 활용한 GPT 프롬포트를 통해 사용자의 입력에 따른 게임 추천 모델로서 활용

---

## 5️⃣Product Serving

### 1) Workflow
<p align="center"><img margin="Auto" width="900" src="https://github.com/boostcampaitech5/level3_recsys_finalproject-recsys-09/assets/44831566/74ca95c0-22d6-426a-965e-153f865148a7"></p>

### 2) FrontEnd

- 사용자 데이터 입력 : 나이, 플랫폼, 선호 장르, 태그, 했던 게임 등
- 게임 추천 결과 출력 : 게임 이름, 플랫폼, 메인 장르, url 등

### 3) BackEnd (FastAPI)

- 웹 서버와 모델 서버로 구성 
- 웹 서버에서 Frontend로부터 사용자 정보를 수신하여 모델 서버에 Request 전송
- 웹 서버에서 모델 서버로부터 Response를 받아 Frontend로 전송

### 4) github-action

- github에 코드 push되면 모델과 웹 서버에 배포 자동화

### 5) redis

- 모델 서버에서의 inference 시간 단축을 위하여 캐시 서버인 redis 서버 사용

### 6) DB

- Frontend의 자동 완성 기능에 사용할 전체 게임 목록 생성
- 모델 서버에서 받은 추천 게임 id 목록을 토대로 Frontend에 제공할 게임 정보 검색
- Frontend로부터 받은 사용자 입력, 모델 서버로부터 받은 모델 출력과 Frontend로부터 받은 사용자 피드백을 저장

---

## 6️⃣ **How to Run**

### run web(local)

```
cd Backend/web/
poetry shell
poetry install
pip install python-multipart
python app.py
```

### run model server(local)

```
cd Backend/backend_model/
poetry shell
poetry install
exit
make run
```

#### You need to make 4 server(Model, Web, DB, Redis)

#### You need to install [Docker](https://docs.docker.com/engine/install/) at model and Web server

## 7️⃣ **Demo (시연 영상)**

<p align="center"><img src="https://github.com/boostcampaitech5/level3_recsys_finalproject-recsys-09/assets/44831566/f487b00f-b20b-4d75-8e71-26776adb191d"></p>


## 8️⃣ Reference

- 자동완성: https://gurtn.tistory.com/212
- Metacritic API: https://github.com/melroy89/metacritic_api
- cookiecutter-fastapi-template: https://github.com/arthurhenrique/cookiecutter-fastapi

## 9️⃣ 팀원 소개


&nbsp;

<table align="center">
  <tr height="155px">
    <td align="center" width="150px">
      <a href="https://github.com/asdftyui"><img src=""/></a>
    </td>
    <td align="center" width="150px">
      <a href="https://github.com/daream2"><img src=""/></a>
    </td>
    <td align="center" width="150px">
      <a href="https://github.com/NongShiN"><img src=""/></a>
    </td>
    <td align="center" width="150px">
      <a href="https://github.com/HeewonKwak"><img src=""/></a>
    </td>
    <td align="center" width="150px">
      <a href="https://github.com/heeManLee"><img src=""/></a>
    </td>
  </tr>
  <tr height="50px">
    <td align="center" width="150px">
      <a href="https://github.com/asdftyui">김현정_T5070</a>
    </td>
    <td align="center" width="150px">
      <a href="https://github.com/daream2">민현지_T5078</a>
    </td>
    <td align="center" width="150px">
      <a href="https://github.com/NongShiN">황찬웅_T5232</a>
    </td>
    <td align="center" width="150px">
      <a href="https://github.com/HeewonKwak">곽희원_T5015</a>
    </td>
    <td align="center" width="150px">
      <a href="https://github.com/heeManLee">이희만_T5169</a>
    </td>
  </tr>
  </tr>
  <tr height="80px">
    <td align="center" width="150px">
      <a>Web Server</a>
    </td>
    <td align="center" width="150px">
      <a>Front End / PM</a>
    </td>
    <td align="center" width="150px">
      <a>Model Enginnering</a>
    </td>
    <td align="center" width="150px">
      <a>Model Server</a>
    </td>
    <td align="center" width="150px">
      <a>Data Enginnering</a>
    </td>
  </tr>
</table>
&nbsp;
