# -*- coding: utf-8 -*- 
# @Time : 2018/7/2 10:14 
# @Author : Allen 
# @Site :  爬取正在热映电影猫眼电影 http://maoyan.com/films
import requests
from maoyan_db import *
from bs4 import BeautifulSoup
import re
from fontTools.ttLib import TTFont
from utils import *
from tqdm import tqdm
from log import LOG


class MAOYAN:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
        }
        self.orm = ORM()
        self.log = LOG()
        self.logger = self.log.get_logger()
        self.logger.info('*'*25)
        self.logger.info("Star:"+datetime.datetime.now().strftime("%Y-%m-%d"))
        self.logger.info('*' * 25)

    def request_movies_info(self):
        url = "http://maoyan.com/films"
        html = requests.get(url=url, headers=self.headers).text
        # save_html('demo_page.html',movie_text)
        '''
            先保存为html文件，对文件写beautifulsoup
        '''
        # html = read_html('demo_pagr.html')
        movies = self.fetch_movie_name_and_url(html)
        # print(type(movies))
        for i in tqdm(range(len(movies))):
            movie_english_name, movie_cat, movie_country, movie_dur, movie_rt, movie_ticket, movie_summary, movie_dir, movie_star = self.request_movie_info(
                movies[i]['movie_url'])
            movies[i]['movie_english_name'] = movie_english_name
            movies[i]['movie_cat'] = movie_cat
            movies[i]['movie_country'] = movie_country
            movies[i]['movie_dur'] = movie_dur
            movies[i]['movie_rt'] = movie_rt
            movies[i]['movie_ticket'] = movie_ticket
            movies[i]['movie_summary'] = movie_summary
            movies[i]['movie_dir'] = movie_dir
            movies[i]['movie_star'] = movie_star
            self.logger.info(movies[i])
            self.orm.insert_movie_info(movies[i])

    def fetch_movie_name_and_url(self, html):
        try:
            movie_names = set(self.orm.query_movie_name())
            bs = BeautifulSoup(html, 'html.parser')
            movies = []
            for dd in bs.find_all('dd'):
                movie_name = dd.find('div', 'channel-detail movie-item-title')['title']
                if not movie_name in movie_names:
                    movie_info = {}
                    movie_info['movie_name'] = movie_name
                    movie_info['movie_url'] = 'http://maoyan.com' + dd.find('div', 'movie-item').a['href']
                    movie_info['movie_image'] = \
                        dd.find('div', 'movie-item').a.find('div', 'movie-poster').find_all('img')[1][
                            'data-src']
                    movie_sc = dd.find('div', 'channel-detail channel-detail-orange').text
                    if '暂无评分' in movie_sc:
                        movie_info['movie_sc'] = 0.0
                    else:
                        movie_info['movie_sc'] = float(movie_sc)
                    movies.append(movie_info)
            return movies
        except:
            self.logger.error("猫眼热门电影错误")

    def request_movie_info(self, url):
        try:
            html = requests.get(url=url, headers=self.headers).text.replace('&#', '0')
            # save_html('demo.html', html)
            # html = read_html('demo.html')
            bs = BeautifulSoup(html, 'html.parser')
            fo = bs.find('div', 'movie-brief-container')
            movie_english_name = fo.find('div', 'ename ellipsis').text.strip()
            fos = fo.ul.find_all('li')
            movie_cat = fos[0].text.strip()
            if ' / ' in fos[1].text:
                movie_country = fos[1].text.split(' / ')[0].strip()
                movie_dur = fos[1].text.split(' / ')[-1].strip()
                regex = re.compile(r'^[1-9]\d*\.\d*|0\.\d*[1-9]\d*$|\d')
                movie_dur = float(''.join(regex.findall(movie_dur)))
            else:
                movie_country = ""
                movie_dur = 0.0
            movie_rt = fos[-1].text.strip()
            # print(movie_english_name)
            # print(movie_cat)
            # print(movie_country)
            # print(movie_dur)
            # print(movie_rt)
            movie_ticket = [i.text for i in
                            bs.find('div', 'movie-stats-container').find('div', 'movie-index-content box').find_all(
                                'span')]
            if '暂无' in movie_ticket:
                movie_ticket = 0.0
            else:
                movie_ticket = self.get_movie_ticket(html)
                movie_ticket = self.unite_ticket(movie_ticket)
            # print(movie_ticket)
            movie_summary = bs.find('div', 'mod-content').span.text.strip()
            # print(movie_summary)
            persons = []
            for i in bs.find_all('div', 'module')[1].find_all('ul', 'celebrity-list clearfix'):
                persons.append([i.a.text.strip() for i in i.find_all('div', 'info')])
            movie_dir = ','.join(persons[0])
            movie_star = ','.join(persons[1])
            # print(movie_dir)
            # print(movie_star)
            return movie_english_name, movie_cat, movie_country, movie_dur, movie_rt, movie_ticket, movie_summary, movie_dir, movie_star
        except:
            self.logger.error("电影主业信息爬取错误")

    '''
        解析票房的字符
    '''

    def get_movie_ticket(self, html, flag=False):
        p = re.compile(r"url\('(.*?)'\) format\('woff'\);")
        uni_font_url = re.findall(p, html)
        url = 'http:%s' % uni_font_url[0]
        # print("字体url：" + url)
        resp = requests.get(url)
        with open('maoyan.woff', 'wb') as fontfile:
            fontfile.write(resp.content)
        baseFonts = TTFont('basefont.woff')  # 这个文件是保存在本地的， 需要手动解析一个字体库， 作为不变的部分
        base_nums = ['4', '1', '3', '0', '5', '6', '7', '9', '2', '8']  # 基本的数字表
        base_fonts = ['uniF66E', 'uniE944', 'uniE4BE', 'uniEF0F', 'uniEF8D', 'uniE963', 'uniE142', 'uniE023',
                      'uniE995',
                      'uniF3A0']  # 基本的映射表
        onlineFonts = TTFont('maoyan.woff')  # 网络上下载的动态的字体文件
        uni_list = onlineFonts.getGlyphNames()[1:-1]  # 只有中间的部分是数字
        temp = {}
        # 解析字体库
        for i in range(10):
            onlineGlyph = onlineFonts['glyf'][uni_list[i]]  # 返回的是unicode对应信息的对象
            for j in range(10):
                baseGlyph = baseFonts['glyf'][base_fonts[j]]
                if onlineGlyph == baseGlyph:
                    temp[uni_list[i].replace('uni', '0x').lower()] = base_nums[j]
        # print(temp)
        for key in temp.keys():
            initstr = key + ';'
            html = html.replace(initstr, str(temp[key]))
        if flag:
            return html
        else:
            return self.find_ticket(html)

    '''
        统一票房单位/万元
    '''

    def find_ticket(self, html):
        bs4 = BeautifulSoup(html, 'html.parser')
        div = bs4.find_all('div', 'movie-index-content box')
        try:
            result = div[0].span.text + div[0].find('span', 'unit').text
            return result
        except:
            self.logger.error("电影票房爬取错误")
            return ''

    def unite_ticket(self, ticket):
        try:
            regex = re.compile(r'^[1-9]\d*\.\d*|0\.\d*[1-9]\d*$|\d')
            num = float(''.join(regex.findall(ticket)))
            if '亿美元' in ticket:
                return num * 10000 * 6.7
            elif '亿' in ticket:
                return num * 1000
            elif '千万' in ticket:
                return num * 100
            elif '十万' in ticket:
                return num * 10
            elif '万美元' in ticket:
                return num * 6.7
            else:
                return num
        except:
            self.logger.error("票房价格转换错误")

    def get_cinema(self, url):
        html = requests.get(url=url, headers=self.headers).text.replace('&#', '0')
        html = self.get_movie_ticket(html, flag=True)
        # save_html('./demo.html', html)
        # html = read_html('./demo.html')
        bs = BeautifulSoup(html, 'html.parser')
        for d in bs.find_all('div', 'show-list'):
            cinema = {}
            movie_name = d.find('h3', 'movie-name').text
            movie_time = datetime.datetime.now().strftime('%Y') + '年' + d.find('span', 'date-item active').text.split()[
                -1]
            cinema['movie_name'] = movie_name
            cinema['movie_time'] = movie_time
            for r in d.find('tbody').find_all('tr'):
                td = r.find_all('td')[:-1]
                movie_open_time = td[0].find('span', 'begin-time').text
                movie_close_time = td[0].find('span', 'end-time').text
                movie_lan = td[1].span.text
                movie_address = td[2].span.text
                movie_price = float(td[3].find('span', 'stonefont').text)
                is_2d, is_3d = self.is3D(movie_lan)
                cinema['movie_open_time'] = movie_open_time
                cinema['movie_close_time'] = movie_close_time
                cinema['movie_lan'] = movie_lan
                cinema['movie_address'] = movie_address
                cinema['movie_price'] = movie_price
                cinema['is_2d'] = is_2d
                cinema['is_3d'] = is_3d
                self.orm.insert_movie_cinema(cinema)
                self.logger.info(cinema)
                # print(movie_name, movie_time, movie_open_time, movie_close_time, movie_lan, movie_address, movie_price,
                #       is_2d, is_3d)

    def is3D(self, value):
        try:
            if '2D' in value.upper():

                return True, False
            else:

                return False, True
        except:

            return False, False


if __name__ == '__main__':
    my = MAOYAN()
    my.request_movies_info()
    my.get_cinema('http://maoyan.com/cinema/13141?poi=6521162')
