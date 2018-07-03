# -*- coding: utf-8 -*- 
# @Time : 2018/7/2 11:23 
# @Author : Allen 
# @Site :  将猫眼电影的相关数据，爬取存入数据库

import pymysql
import time

def connection():
    return pymysql.connect(host='192.168.160.36', port=3306,
                                  user='root', passwd='gzxiaoi', db='crawler', charset='utf8')

def insert_db(movie):
    conn = connection()
    cursor = conn.cursor()
    sql = '''
    INSERT INTO MAOYAN_MOVIES(NAME_MOVIES,CAT,DUR,SC,RT,IMG,MOVIE_ID,CRAWL_TIME)
    VALUES('%s','%s',%f,%f,'%s','%s',%d,'%s')
    '''
    try:

        cursor.execute(sql%(movie['nm'],movie['cat'],movie['dur'],movie['sc'],movie['rt'],
                            movie['img'],movie['id'],time.strftime("%Y-%m-%d")))
        conn.commit()
        # print("Sucess insert: %s"%(movie['nm']))
    except Exception as e:
        print(e)
    else:
        conn.close()
        cursor.close()

def insert_movie_info(a,b,c,d,e,f,g):
    conn = connection()
    cursor = conn.cursor()
    sql = '''
        INSERT INTO MOVIES_INFO(MOVIE_NAME,MOVIE_OPEN_TIME,MOVIE_CLOSE_TIME,MOVIE_LAN,MOVIE_ADDRESS,IS_3D,IS_2D)
        VALUES('%s','%s','%s','%s','%s',%d,%d)
    '''
    try:
        cursor.execute(sql%(a,b,c,d,e,f,g))
        conn.commit()
    except Exception as e:
        print(e)
    else:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    insert_db()