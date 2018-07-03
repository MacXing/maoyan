# -*- coding: utf-8 -*- 
# @Time : 2018/7/2 10:14 
# @Author : Allen 
# @Site :  爬取猫眼电影api http://m.maoyan.com/movie/list.json?type=hot&offset=0&limit=1
import requests
import json
from maoyan_db import *
from bs4 import BeautifulSoup
import re

def request_movies():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    url = "http://m.maoyan.com/movie/list.json?type=hot&offset=0&limit=1000"
    cinemas_url = 'http://maoyan.com/cinemas'
    movies = requests.get(url=url,headers = headers).text
    movies = json.loads(movies)['data']['movies']
    for movie in movies:
        # insert_db(movie)
        print(movie)

def get_cinema():
    url = "http://maoyan.com/cinema/13141?poi=6521162"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    cinema_data = requests.get(url=url,headers=headers).text
    clear_data(cinema_data)

def clear_data(html):
    bs = BeautifulSoup(html,'html.parser')
    movie_infos = bs.find_all('div','show-list')
    movies_dict={}
    for movie_info in movie_infos:
        movie_name = movie_info.div.h3.text
        movies_dict['movie_name'] = movie_name
        print(movie_info.div.h3.text)
        movie_time = list()
        movie_lan = []
        movie_address = []
        for plist in movie_info.find_all('div','plist-container active'):
            for trs in plist.find_all('tbody'):
                for tr in trs.find_all('tr'):
                    is_3d = False
                    is_2d = True
                    movie_num = tr.find_all('td')[0].text.split()
                    movie_time.append(movie_num)
                    movie_language = tr.find_all('td')[1].text.replace('\n','')
                    movie_lan.append(movie_language)
                    movie_hall = tr.find_all('td')[2].text.replace('\n','')
                    movie_address.append(movie_hall)
                    if '3D' in movie_language:
                        is_3d = True
                        is_2d = False
                    print(movie_name+" "+' '.join(movie_num)+" "+movie_language+" "+movie_hall)
                    insert_movie_info(movie_name,movie_num[0],movie_num[1],movie_language,movie_hall,is_3d,is_2d)
        movies_dict['movie_info'] = [movie_time,movie_lan,movie_address]
        print(movies_dict)



if __name__ == '__main__':
    # request_movies()
    get_cinema()
