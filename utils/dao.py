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


def get_grid_finished(db, date, date_plus1):
    cur = db.connection.cursor()
    sql = "select a.网格, count(*) cnt from (" \
          "select r.网格, r.证件号码 from residents r " \
          "join covid_detection_records cdr " \
          "on r.证件号码 = cdr.证件号码 " \
          f"and  cdr.采样时间 > '{date}' " \
          f"and cdr.采样时间 < '{date_plus1}') a " \
          "group by a.网格;"
    return sql_query(sql, cur)


# people
def get_whitelist(db):
    cur = db.connection.cursor()
    sql = "select * from residents;"
    return sql_query(sql, cur)


def get_grey_list(db):
    cur = db.connection.cursor()
    sql = "select * from residents where 是否在白名单='是' and 是否在灰名单='是';"
    return sql_query(sql, cur)


def get_grid_whitelist_people(db, grid):
    cur = db.connection.cursor()
    sql = f"select * from residents r where r.网格 = '{grid}';"
    return sql_query(sql, cur)


def get_records_position(db, date, date_plus1):
    cur = db.connection.cursor()
    sql = "select cdr.采样地点,cdr.采样时间 from residents r " \
          "join covid_detection_records cdr " \
          "on r.证件号码 = cdr.证件号码 " \
          f"and  cdr.采样时间 > '{date}' " \
          f"and cdr.采样时间 < '{date_plus1}'" \
          "and locate('浪心', cdr.采样地点) > 0 ;"
    return sql_query(sql, cur)


def get_grids_record_time(db, limit_date):
    cur = db.connection.cursor()
    sql = "select r.网格, r.上次核酸检测时间 from residents r " \
          "where r.是否在白名单 = '是' " \
          f"and (r.上次核酸检测时间 is not null and r.上次核酸检测时间 > '{limit_date}');"
    return sql_query(sql, cur)


def sql_query(sql, cur):
    cur.execute(sql)
    data = cur.fetchall()
    return data
