# test for load_data.py: compare result with ground truth
import datetime
import os
import sys

sys.path.append(os.getcwd() + '/../..')
from modules.database.ConnectingPool import getConnectionPool


def whitelist_rownum_test(cp):
    whitelist_date_rownum_dict = {'2022-07-27': 65288, '2022-08-18': 65288, '2022-08-19': 65700, '2022-08-23': 65700,
                                  '2022-08-24': 62963, '2022-08-25': 62568, '2022-09-07': 62568, '2022-09-08': 64813,
                                  '2022-09-09': 64549, '2022-09-12': 64549, '2022-09-13': 64347, '2022-09-14': 65179,
                                  '2022-09-15': 65258, '2022-09-16': 65130, '2022-09-17': 65130, '2022-09-18': 65102,
                                  '2022-09-19': 65282, '2022-09-20': 65416, '2022-09-21': 65241, '2022-09-22': 65241}
    query_sql = "select count(*) from residents where 加入白名单时间 <= '{date}' and (移出白名单时间 >= '{date}' or 移出白名单时间 is null);"

    try:
        conn = cp.get_connection()
        cursor = conn.cursor()
        for date in whitelist_date_rownum_dict.keys():
            certain_query_sql = query_sql.replace('{date}', date)
            ground_truth = whitelist_date_rownum_dict.get(date)
            cursor.execute(certain_query_sql)
            row_num = cursor.fetchone()[0]
            if int(row_num) != int(whitelist_date_rownum_dict.get(date)):
                print('Test whitelist_rownum_test Fails: row num of whitelist in %s not match ground truth, '
                      'query result is %d, ground truth is %d.' % (date, row_num, ground_truth))
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def whitelist_accumulate_rownum_test(cp):
    whitelist_date_rownum_dict = {'2022-07-27': 65288, '2022-08-19': 65700, '2022-08-24': 62963, '2022-08-25': 62568,
                                  '2022-09-08': 64813, '2022-09-09': 64549, '2022-09-13': 64347, '2022-09-14': 65179,
                                  '2022-09-15': 65258, '2022-09-16': 65130, '2022-09-18': 65102, '2022-09-19': 65282,
                                  '2022-09-20': 65416}
    query_sql = "select count(*) from residents_accumulative where 加入白名单时间 = '{date}' ;"

    try:
        conn = cp.get_connection()
        cursor = conn.cursor()
        for date in whitelist_date_rownum_dict.keys():
            certain_query_sql = query_sql.replace('{date}', date)
            ground_truth = whitelist_date_rownum_dict.get(date)
            cursor.execute(certain_query_sql)
            row_num = cursor.fetchone()[0]
            if int(row_num) != int(whitelist_date_rownum_dict.get(date)):
                print('Test whitelist_rownum_test Fails: row num of whitelist in %s not match ground truth, '
                      'query result is %d, ground truth is %d.' % (date, row_num, ground_truth))
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def whitelist_covid_detection_test(cp):
    covid_detection_dates = {'2022-09-16', '2022-09-18', '2022-09-19', '2022-09-20'}
    covid_detection_ground_truth = {1: {'2022-09-16': 46435, '2022-09-18': 52352, '2022-09-19': 43078, '2022-09-20': 41949}}

    sql = '''
    select
        count(distinct r.证件号码,房屋编码)
    from
        langxin_community.residents r left join
        langxin_community.covid_detection_records cdr
    on
        r.证件号码 = cdr.证件号码
    where
        cdr.证件号码 is not null and
        r.加入白名单时间 <= '{date}' and
        (r.移出白名单时间 >= '{date}' or r.移出白名单时间 is null) and
        cdr.采样时间 <= DATE_ADD('{date}', INTERVAL 1 day) and 采样时间 >= DATE_SUB('{date}', INTERVAL {interval} DAY);
    '''

    conn = cp.get_connection()
    cursor = conn.cursor()
    for interval in covid_detection_ground_truth.keys():
        for date in covid_detection_ground_truth.get(interval):
            certain_sql = sql.replace('{date}', date).replace('{interval}', str(interval-1))
            cursor.execute(certain_sql)
            result = cursor.fetchone()[0]
            ground_truth = covid_detection_ground_truth.get(interval).get(date)
            if int(result) != ground_truth:
                print('Test covid_detection_test Fails: count of covid detection in %s with interval as %d not match '
                      'ground truth, query result is %d, ground truth is %d.' % (date, interval, result, ground_truth))
    cursor.close()
    conn.close()


def whitelist_accumulative_covid_detection_test(cp):
    covid_detection_dates = {'2022-09-16', '2022-09-18', '2022-09-19', '2022-09-20'}
    covid_detection_ground_truth = {1: {'2022-09-16': 46435, '2022-09-18': 52352, '2022-09-19': 43078, '2022-09-20': 41949}}

    sql = '''
    select count(*) from residents_accumulative
    where 加入白名单时间 = '{date}' and 上次核酸检测时间 >= DATE_SUB('{date}', INTERVAL {interval} DAY ) and 上次核酸检测时间 < DATE_ADD('{date}', INTERVAL 1 DAY);
    '''

    conn = cp.get_connection()
    cursor = conn.cursor()
    for interval in covid_detection_ground_truth.keys():
        for date in covid_detection_ground_truth.get(interval):
            certain_sql = sql.replace('{date}', date).replace('{interval}', str(interval-1))
            cursor.execute(certain_sql)
            result = cursor.fetchone()[0]
            ground_truth = covid_detection_ground_truth.get(interval).get(date)
            if int(result) != ground_truth:
                print('Test covid_detection_test Fails: count of covid detection in %s with interval as %d not match '
                      'ground truth, query result is %d, ground truth is %d.' % (date, interval, result, ground_truth))
    cursor.close()
    conn.close()


def fetch_null_test(cp):
    date = '2022-07-26'
    get_next_add_time_sql = "select min(加入白名单时间) from langxin_community.residents where 加入白名单时间 > '{date}'".replace('{date}', date)
    get_next_remove_time_sql = "select min(移出白名单时间) from langxin_community.residents where 移出白名单时间 > '{date}'".replace('{date}', date)
    remove_time = 'null'
    try:
        conn = cp.get_connection()
        cursor = conn.cursor()
        cursor.execute(get_next_add_time_sql)
        next_add_time = cursor.fetchone()[0]
        cursor.execute(get_next_remove_time_sql)
        next_remove_time = cursor.fetchone()[0]
        print(type(next_add_time), type(next_remove_time))
        if next_add_time is None and next_remove_time is None:
            remove_time = 'null'
        elif next_add_time is None:
            remove_time = "'" + next_remove_time.strftime("%Y-%m-%d %H:%M:%S") + "'"
        elif next_remove_time is None:
            remove_time = "'" + (next_add_time - datetime.timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S") + "'"
        else:
            if next_add_time < next_remove_time:
                remove_time = "'" + (next_add_time - datetime.timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S") + "'"
            else:
                remove_time = "'" + next_remove_time.strftime("%Y-%m-%d %H:%M:%S") + "'"
        print("remove_time =", remove_time)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    connectionPool = getConnectionPool()

    # whitelist_rownum_test(connectionPool)

    whitelist_accumulate_rownum_test(connectionPool)

    # whitelist_covid_detection_test(connectionPool)

    whitelist_accumulative_covid_detection_test(connectionPool)

    # fetch_null_test(connectionPool)

    print('all tests finished!')
