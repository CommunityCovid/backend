import json
import random
import pymysql


def get_whitelist_num(db, date, date_plus1):
    cur = db.connection.cursor()

    sql = "select count(*) cnt from langxin_community.residents_accumulative where 加入白名单时间 = '{date}';"
    sql = sql.replace('{date}', date)

    data = sql_query(sql, cur)
    return data[0]["cnt"]


def get_greylist_num(db, date, date_plus1):
    cur = db.connection.cursor()

    sql = "select count(*) cnt from langxin_community.residents_accumulative where 加入白名单时间 = '{date}' and 是否在灰名单 = '是';"
    sql = sql.replace('{date}', date)

    data = sql_query(sql, cur)
    return data[0]["cnt"]


def get_finished_num(db, date, record_limit):
    cur = db.connection.cursor()

    sql = '''
        select count(*) cnt from langxin_community.residents_accumulative
        where 加入白名单时间 = '{date}' and
          上次核酸检测时间 < DATE_ADD('{date}', INTERVAL 1 DAY) and
          上次核酸检测时间 >= DATE_SUB('{date}', INTERVAL {interval} DAY );
        '''
    sql = sql.replace('{date}', date).replace('{interval}', str(record_limit - 1))

    data = sql_query(sql, cur)
    return data[0]["cnt"]


def get_finished_grey_num(db, date, record_limit):
    cur = db.connection.cursor()
    sql = '''
        select count(*) cnt from langxin_community.residents_accumulative
        where 加入白名单时间 = '{date}' and
            是否在灰名单='是' and
            上次核酸检测时间 < DATE_ADD('{date}', INTERVAL 1 DAY) and
            上次核酸检测时间 >= DATE_SUB('{date}', INTERVAL {interval} DAY );
        '''
    sql = sql.replace('{date}', date).replace('{interval}', str(record_limit - 1))

    data = sql_query(sql, cur)
    return data[0]["cnt"]


def get_grid_whitelist(db, date):
    cur = db.connection.cursor()
    sql = '''
        select 网格, count(*) cnt from langxin_community.residents_accumulative r
        where 加入白名单时间 = '{date}' group by 网格;
        '''
    sql = sql.replace('{date}', date)

    return sql_query(sql, cur)


def get_grid_grey_whitelist(db, date):
    cur = db.connection.cursor()
    sql = '''
        select 网格, count(*) cnt from langxin_community.residents_accumulative r
        where 加入白名单时间 = '{date}' and 是否在灰名单='是'
        group by 网格;
        '''
    sql = sql.replace('{date}', date)

    return sql_query(sql, cur)


def get_housings_whitelist(db, date):
    cur = db.connection.cursor()
    sql = '''
        select 小区, count(*) cnt from langxin_community.residents_accumulative r
        where 加入白名单时间 = '{date}' and 小区 is not null 
        group by 小区;
        '''
    sql = sql.replace('{date}', date)

    return sql_query(sql, cur)


def get_grids(db, date):
    cur = db.connection.cursor()
    sql = "select distinct 网格 from langxin_community.residents_accumulative;"
    return sql_query(sql, cur)


def get_housing(db):
    cur = db.connection.cursor()
    sql = "select distinct 小区 from langxin_community.residents_accumulative;"
    return sql_query(sql, cur)


def get_community_whitelist(db, date):
    cur = db.connection.cursor()
    sql = '''
        select 小区, count(*) cnt from langxin_community.residents_accumulative r
        where 加入白名单时间 = '{date}' and 小区 is not null 
        group by 小区;
        '''
    sql = sql.replace('{date}', date)

    return sql_query(sql, cur)


def get_grid_finished(db, date, record_limit):
    cur = db.connection.cursor()
    sql = '''
        select 网格, count(*) cnt from langxin_community.residents_accumulative
        where 加入白名单时间 = '{date}' and
          上次核酸检测时间 < DATE_ADD('{date}', INTERVAL 1 DAY) and
          上次核酸检测时间 >= DATE_SUB('{date}', INTERVAL {interval} DAY )
        group by 网格;
        '''
    sql = sql.replace('{date}', date).replace('{interval}', str(record_limit - 1))

    return sql_query(sql, cur)


def get_grid_grey_finished(db, date, record_limit):
    cur = db.connection.cursor()
    sql = '''
        select 网格, count(*) cnt from langxin_community.residents_accumulative
        where 加入白名单时间 = '{date}' and
            是否在灰名单 = '是' and
            上次核酸检测时间 < DATE_ADD('{date}', INTERVAL 1 DAY) and
            上次核酸检测时间 >= DATE_SUB('{date}', INTERVAL {interval} DAY )
        group by 网格;
        '''
    sql = sql.replace('{date}', date).replace('{interval}', str(record_limit - 1))

    return sql_query(sql, cur)


def get_housing_finished(db, date, record_limit):
    cur = db.connection.cursor()
    sql = '''
        select 小区, count(*) cnt from langxin_community.residents_accumulative
        where 加入白名单时间 = '{date}' and
            上次核酸检测时间 < DATE_ADD('{date}', INTERVAL 1 DAY) and
            上次核酸检测时间 >= DATE_SUB('{date}', INTERVAL {interval} DAY ) and
            小区 is not null
        group by 小区;
        '''
    sql = sql.replace('{date}', date).replace('{interval}', str(record_limit - 1))

    return sql_query(sql, cur)


# people
def get_whitelist(db):
    cur = db.connection.cursor()
    sql = "select * from langxin_community.residents_accumulative;"
    return sql_query(sql, cur)


def get_grey_list(db, date):
    cur = db.connection.cursor()
    sql = "select * from langxin_community.residents_accumulative where 加入白名单时间 = '{date}' and 是否在灰名单='是';"
    sql = sql.replace('{date}', date)
    return sql_query(sql, cur)


def get_grid_whitelist_people(db, date, grid):
    cur = db.connection.cursor()
    sql = '''
        select * from langxin_community.residents_accumulative
        where 加入白名单时间 = '{date}' and 网格 = '{grid}';
        '''
    sql = sql.replace('{date}', date).replace('{grid}', grid)

    return sql_query(sql, cur)


def get_grid_greylist_people(db, date, grid):
    cur = db.connection.cursor()
    sql = '''
            select * from langxin_community.residents_accumulative
            where 加入白名单时间 = '{date}' and 网格 = '{grid}' and 是否在灰名单 = '是';
            '''
    sql = sql.replace('{date}', date).replace('{grid}', grid)
    return sql_query(sql, cur)


def get_records_position(db, date, date_plus1):
    cur = db.connection.cursor()
    sql = f"select 采样地点, 采样时间 from langxin_community.covid_detection_records "\
            f"where 采样时间 >= '{date}' and 采样时间 < '{date_plus1}' and locate('浪心', 采样地点) > 0; "
    return sql_query(sql, cur)


def get_grids_record_time(db, date, limit_date):
    cur = db.connection.cursor()
    sql = "select 网格, 上次核酸检测时间 from langxin_community.residents_accumulative " \
          f"where 加入白名单时间 = '{date}' " \
          f"and (上次核酸检测时间 is not null and 上次核酸检测时间 > '{limit_date}');"
    return sql_query(sql, cur)


def get_housing_record_time(db, date, limit_date):
    cur = db.connection.cursor()
    sql = "select 小区, 上次核酸检测时间 from langxin_community.residents_accumulative " \
          f"where 加入白名单时间 = '{date}' " \
          f"and (上次核酸检测时间 is not null and 上次核酸检测时间 > '{limit_date}')" \
          f"and 小区 is not null;"
    return sql_query(sql, cur)


def get_community_record_time(db, date, limit_date):
    cur = db.connection.cursor()
    sql = "select 小区, 上次核酸检测时间 from langxin_community.residents_accumulative " \
          f"where 加入白名单时间 = '{date}' " \
          f"and (上次核酸检测时间 is not null and 上次核酸检测时间 > '{limit_date}')" \
          f"and 小区 is not null;"
    return sql_query(sql, cur)


def get_grids_charge(db):
    cur = db.connection.cursor()
    sql = "select * from grid_administrators;"
    return sql_query(sql, cur)


def sql_query(sql, cur):
    cur.execute(sql)
    data = cur.fetchall()
    return data
