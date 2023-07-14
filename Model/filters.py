import pandas as pd
import numpy as np

def age_filter(df, age):
    ratings = {
        9: ['all'],
        10: ['all', '10+'],
        13: ['all', '10+', '13+'],
        17: ['all', '10+', '13+', '17+'],
        20: ['all', '10+', '13+', '17+', '20+']
    }
    conditions = [df['rating'].isin(ratings[a]) for a in ratings if a <= age]
    return df[np.any(conditions, axis=0)]
    
    
def players_filter(df, players):
    # num_of_player_idx 열의 비트와 필터링할 플레이어 수의 비트를 비교하여 필터링
    if players == 5:
        return df[df['num_of_player_idx'] == 5]
    elif players == 4:
        return df[(df['num_of_player_idx'] & 12) != 0]  # 12 = 4 | 8
    elif players == 2:
        return df[(df['num_of_player_idx'] & 14) != 0]  # 14 = 2 | 4 | 8
    else:  # players == 1:
        return df


def platform_and_genre_filter(df_, platform, major_genre):
    """ 
    - input example -
    platform = ['PC', 'iOS', 'Switch']
    major_genre = ['AOS']"""

    df = df_.copy()
    df['split_genres'] = df['major_genre'].fillna('NaN').apply(lambda genres: genres.split(','))
    df['split_platform'] = df['platform'].fillna('NaN').apply(lambda platform: platform.split(','))

    idx_arr = []
    for genre, platforms, idx in zip(df['split_genres'],df['split_platform'], df['id']):
        i_ = [x.strip() for x in genre]
        j_ = [y.strip() for y in platforms]

        if any(x in i_ for x in major_genre) and any(y in j_ for y in platform): idx_arr.append(idx)

    # 'split_genres', 'split_platform' 열을 삭제
    df = df.drop('split_genres', axis=1)
    df = df.drop('split_platform', axis=1)
    return df[df['id'].isin(idx_arr)]
    
    
def filter (df, age, platform, players, major_genre):
    output = platform_and_genre_filter(df, platform, major_genre)
    output = players_filter(output, players)
    output = age_filter(output, age)
    #return output
    return output['id']