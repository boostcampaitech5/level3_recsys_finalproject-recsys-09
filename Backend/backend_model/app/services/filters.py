import pandas as pd


def age_filter(df, age):
    if age == 9:
        return df[df['rating'].isin(['all'])]
    elif age == 10:
        return df[df['rating'].isin(['all', '10+'])]
    elif age == 13:
        return df[df['rating'].isin(['all', '10+', '13+'])]
    elif age == 17:
        return df[df['rating'].isin(['all', '10+', '13+', '17+'])]
    else: # age == 20:
        return df
    
    
def players_filter(df, players):
    conditions = {
        5: df['num_of_player_idx'] == 5,
        4: df['num_of_player_idx'].isin([4, 5]),
        2: df['num_of_player_idx'].isin([2, 4, 5])
    }
    if players in conditions:
        condition = conditions[players]
        return df[condition]
    else:
        return df
    

def platform_and_genre_filter(df_, platform, major_genre):
    df = df_.copy()
    df['split_genres'] = df['major_genre'].fillna('NaN').apply(lambda genres: genres.split(','))
    df['split_platform'] = df['platform'].fillna('NaN').apply(lambda platform: platform.split(','))

    idx_arr = []
    for genre, platforms, idx in zip(df['split_genres'],df['split_platform'], df['id']):
        i_ = [x.strip() for x in genre]
        j_ = [y.strip() for y in platforms]

        if any(x in i_ for x in major_genre) and any(y in j_ for y in platform): idx_arr.append(idx)

    # 'split_genres' 열을 삭제
    df = df.drop('split_genres', axis=1)
    df = df.drop('split_platform', axis=1)
    return  df[df['id'].isin(idx_arr)]

def platform_filter(df_, platform):
    # major_genre 열에서 각 장르를 개별적으로 추출하여 새로운 열인 'split_genres'에 저장
    df = df_.copy()
    df['split_platform'] = df['platform'].fillna('NaN').apply(lambda platform: platform.split(','))
    
    idx_arr = []
    for platforms, idx in zip(df['split_platform'], df['id']):
        i_ = [x.strip() for x in platforms]
        if any(x in i_ for x in platform): idx_arr.append(idx)

    # 'split_genres' 열을 삭제
    df = df.drop('split_platform', axis=1)
    return  df[df['id'].isin(idx_arr)]
    

def filter (df, age, platform, players, major_genre, type):
    if type == 'cb':
        output = platform_and_genre_filter(df, platform, major_genre)
    else: # cf
        output = platform_filter(df, platform)
    output = players_filter(output, players)
    output = age_filter(output, age)

    return output['id']