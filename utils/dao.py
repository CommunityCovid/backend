import json
import random

import numpy as np
import pymysql
import pandas as pd


def get_whitelist_num(db):
    cur = db.connection.cursor()
    sql = "select count(*) cnt from residents;"
    data = sql_query(sql, cur)
    return data[0]["cnt"]


def get_finished_num(db):
    cur = db.connection.cursor()
    sql = "select count(distinct r.id) cnt from residents r " \
          "join covid_detection_records cdr " \
          "on r.证件号码 = cdr.证件号码;"
    data = sql_query(sql, cur)
    return data[0]["cnt"]


def get_grid_whitelist(db, date):
    cur = db.connection.cursor()
    sql = "select r.网格, count(*) cnt from residents r " \
          "group by r.网格;"
    return sql_query(sql, cur)


def get_grid_finished(db, date):
    cur = db.connection.cursor()
    sql = "select a.网格, count(*) cnt from (" \
          "select r.网格, r.证件号码 from residents r " \
          "join covid_detection_records cdr " \
          "on r.证件号码 = cdr.证件号码 " \
          "and  cdr.采样时间 > '2022-08-25' " \
          "and cdr.采样时间 < '2022-08-26') a " \
          "group by a.网格;"
    return sql_query(sql, cur)


# people
def get_whitelist(db):
    cur = db.connection.cursor()
    sql = "select * from residents;"
    return sql_query(sql, cur)


def get_grid_whitelist_people(db, grid):
    cur = db.connection.cursor()
    sql = f"select * from residents r where r.网格 = '{grid}';"
    return sql_query(sql, cur)


def get_records_position(db):
    cur = db.connection.cursor()
    sql = "select cdr.采样地点,cdr.采样时间 from residents r " \
          "join covid_detection_records cdr " \
          "on r.证件号码 = cdr.证件号码 " \
          "and  cdr.采样时间 > '2022-08-25' " \
          "and cdr.采样时间 < '2022-08-26'" \
          "and locate('浪心', cdr.采样地点) > 0 ;"
    return sql_query(sql, cur)


def sql_query(sql, cur):
    cur.execute(sql)
    data = cur.fetchall()
    return data
