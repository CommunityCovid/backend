import json
import random

import numpy as np
import pymysql
import pandas as pd

DATABASE = "langxin_community"
USER = "root"
PASSWORD = "root"
HOST = "10.20.4.104"
PORT = 3306


class DBServer:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.init_db_connect()

    def test_cnt(self):
        return pd.read_sql("select * from residents limit 10", self.conn)

    def init_db_connect(self):
        self.conn = pymysql.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
        self.cur = self.conn.cursor()

    def close(self):
        print("Database connection is closed")
        self.conn.commit()
        self.conn.close()

    def get_whitelist_num(self):
        sql = "select count(*) cnt from residents;"
        return pd.read_sql(sql, self.conn)['cnt'][0]

    def get_whitelist(self):
        sql = "select * from residents;"
        return pd.read_sql(sql, self.conn)

    def get_grid_whitelist_people(self, grid):
        sql = f"select * from residents r where r.网格 = '{grid}';"
        return pd.read_sql(sql, self.conn)

    def get_finished_num(self):
        sql = "select count(distinct r.id) cnt from residents r " \
              "join covid_detection_records cdr " \
              "on r.证件号码 = cdr.证件号码;"
        return pd.read_sql(sql, self.conn)['cnt'][0]

    def get_grid_whitelist(self, date):
        sql = "select r.网格, count(*) cnt from residents r " \
              "group by r.网格;"
        return pd.read_sql(sql, self.conn)

    def get_grid_finished(self, date):
        sql = "select a.网格, count(*) cnt from (" \
              "select r.网格, r.证件号码 from residents r " \
              "join covid_detection_records cdr " \
              "on r.证件号码 = cdr.证件号码 " \
              "and  cdr.采样时间 > '2022-08-25' " \
              "and cdr.采样时间 < '2022-08-26') a " \
              "group by a.网格;"
        return pd.read_sql(sql, self.conn)

    def get_community_people(self):
        sql = ""
