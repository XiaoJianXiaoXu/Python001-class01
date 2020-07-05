# 使用BeautifulSoup解析网页

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'


header = {'user-agent':user_agent}

myurl = 'https://maoyan.com/films?showType=3'

response = requests.get(myurl,headers=header)

bs_info = bs(response.text, 'html.parser')
#print(bs_info)
movie_list10 = []



for tags in bs_info.find_all('div', attrs={'class': 'movie-item-hover'})[:10]:

    for item in tags.find_all('div', attrs={'class': 'movie-hover-info'}):

        movie_name = item.find('span', attrs={'class': 'name'}).text    # 电影名称
        
        content = item.find_all('span', attrs={'class':'hover-tag'})

        movie_type = content[0].next_sibling.strip()    # 电影类型

        movie_time = content[2].next_sibling.strip()  # 上映时间

        movie_list10.append([movie_name, movie_type, movie_time])



movies = pd.DataFrame(data=movie_list10, columns=['电影名称', '电影类型', '上映时间'])

#print(movies)

movies.to_csv('./maoyanmovies.csv', encoding='gbk', index=False, header=False)
