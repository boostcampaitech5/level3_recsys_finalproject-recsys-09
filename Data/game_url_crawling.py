from bs4 import BeautifulSoup
import requests
import pandas as pd
from MetaCriticScraper import MetaCriticScraper


years = [i for i in range(2000, 2023)]

for y in years:
    year = str(y)

    hrd = {'User-Agent' : 'Mozilla/5.0', 'referer' : 'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=' + year + '&distribution=&sort=desc&view=detailed'}
    url = "https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=" + year + "&distribution=&sort=desc&view=detailed"

    req = requests.get(url, headers=hrd)

    soup = BeautifulSoup(req.content, "html.parser", from_encoding='utf-8')
    questions = soup.find("div", {"class":"title_bump"})

    d = list(questions.find_all("a", class_="page_num"))
    url_num_list = [int(item.string.strip()) for item in d]

    num_list = []
    for i in range(url_num_list[len(url_num_list)-1]):
        num_list.append(str(i))


    df_url = pd.DataFrame(columns=['game', 'url'])

    for j in range(len(num_list)):
        hrd = {'User-Agent' : 'Mozilla/5.0', 'referer' : "https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=" + year + "&distribution=&sort=desc&view=detailed" + "&page=" + num_list[j] }
        url = "https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=" + year + "&distribution=&sort=desc&view=detailed" + "&page=" + num_list[j]

        req = requests.get(url, headers=hrd)

        soup = BeautifulSoup(req.content, "html.parser", from_encoding='utf-8')
        # 게임 목록을 가져오기 위해 필요한 태그와 클래스를 확인합니다.
        game_items = soup.find_all("td", class_="clamp-summary-wrap")

        # 각 게임별 URL을 추출합니다.       
        for item in game_items:
            link = item.find("a", class_="title")
            game_name_url = 'https://www.metacritic.com' + link['href']
            game_name = MetaCriticScraper(game_name_url).game['title']

            url_tmp = pd.DataFrame(columns=['game', 'url'])
            url_tmp.loc[0] = [game_name, game_name_url]
            df_url = pd.concat([df_url, url_tmp])

    # csv로 저장
    df_url.to_csv('./data/url/' + year + '_url.csv', index=False)