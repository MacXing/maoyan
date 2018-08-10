# -*- coding: utf-8 -*- 
# @Time : 2018/7/2 11:23 
# @Author : Allen 
# @Site :  将猫眼电影的相关数据，爬取存入数据库
import uuid
import time

import datetime
from sqlalchemy import Column, String, create_engine, Text, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class YSFZ_MANAGER_MOVIES(declarative_base()):
    __tablename__ = 'YSFZ_MANAGER_MOVIES'
    id = Column(String(100), primary_key=True)
    movie_name = Column(String(255))
    movie_english_name = Column(String(255))
    movie_country = Column(String(50))
    movie_summary = Column(Text)
    movie_dir = Column(String(255))
    movie_ticket = Column(Float)
    movie_star = Column(String(255))
    movie_cat = Column(String(255))
    movie_dur = Column(Float)
    movie_sc = Column(Float)
    movie_rt = Column(String(50))
    movie_img = Column(String(100))
    crawl_time = Column(String(50))
    movie_url = Column(String(100))


class ORM:
    def __init__(self):
        # 初始化数据库连接:
        self.engine = create_engine('mysql+mysqldb://root:soif*324#fsIIH@172.16.205.46:3306/YSFZ_MANAGER?charset=utf8')
        # 创建DBSession类型:
        self.DBSession = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.DBSession()

    def close_session(self):
        self.get_session().close()

    def commit_session(self):
        self.get_session().commit()

    def query_movie_name(self):
        return [d[0] for d in self.get_session().query(YSFZ_MANAGER_MOVIES.movie_name).all()]

    def insert_movie_info(self, movie):
        session =self.DBSession()
        session.add(YSFZ_MANAGER_MOVIES(
            id=''.join(str(uuid.uuid4()).replace('-', '')),
            movie_name=movie['movie_name'],
            movie_english_name=movie['movie_english_name'],
            movie_country=movie['movie_country'],
            movie_summary=movie['movie_summary'],
            movie_dir=movie['movie_dir'],
            movie_ticket=movie['movie_ticket'],
            movie_star=movie['movie_star'],
            movie_cat=movie['movie_cat'],
            movie_dur=movie['movie_dur'],
            movie_sc=movie['movie_sc'],
            movie_rt=movie['movie_rt'],
            movie_img=movie['movie_image'],
            crawl_time=datetime.datetime.now().strftime('%Y-%m-%d'),
            movie_url=movie['movie_url']
        ))
        session.commit()
        session.close()


if __name__ == '__main__':
    orm = ORM()
    print(orm.query_movie_name())
