import pandas as pd


def age_filter(df, age):
    if age == 9:
        return df[df['rating'] == 'all']
    elif age == 10:
        return df[(df['rating'] == 'all') | (df['rating'] == '10+')]
    elif age == 13:
        return df[(df['rating'] == 'all') | (df['rating'] == '10+') | (df['rating'] == '13+')]
    elif age == 17:
        return df[(df['rating'] == 'all') | (df['rating'] == '10+') | (df['rating'] == '13+') | (df['rating'] == '17+')]
    else: # age == 20:
        return df
    
    
def players_filter(df, players):
    return df[df['num_of_player_idx'] == players]


def platform_and_genre_filter(df_, platform, major_genre):
    df = df_.copy()
    df['split_genres'] = df['major_genre'].fillna('NaN').apply(lambda genres: genres.split(','))
    df['split_platform'] = df['platform'].fillna('NaN').apply(lambda platform: platform.split(','))

    idx_arr = []
    for genre, platforms, idx in zip(df['split_genres'],df['split_platform'], df['id']):
        i_ = [x.strip() for x in genre]
        j_ = [y.strip() for y in platforms]

        if any(x in i_ for x in major_genre) and any(y in j_ for y in platform): idx_arr.append(idx-1)

    # 'split_genres' 열을 삭제
    df = df.drop('split_genres', axis=1)
    df = df.drop('split_platform', axis=1)
    return df.loc[idx_arr]
    

def major_genre_filter(df_, major_genre):
    # major_genre 열에서 각 장르를 개별적으로 추출하여 새로운 열인 'split_genres'에 저장
    df = df_.copy()
    df['split_genres'] = df['major_genre'].apply(lambda genres: genres.split(','))
    
    idx_arr = []
    for genre, idx in zip(df['split_genres'], df['id']):
        i_ = [x.strip() for x in genre]
        if any(x in i_ for x in major_genre): idx_arr.append(idx-1)

    # 'split_genres' 열을 삭제
    #df = df.drop('split_genres', axis=1)
    
    return df_.loc[idx_arr]
    

def filter (df, age, platform, players, major_genre):
    output = platform_and_genre_filter(df, platform, major_genre)
    output = players_filter(output, players)
    output = age_filter(output, age)

    return output['id']