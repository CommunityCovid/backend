import os
import sys
import time

sys.path.append('./')
from modules.database.ConnectingPool import getConnectionPool

create_database_sql_dir = 'modules/database/database_creation_sql/'


def create_database():
    start_time = time.time()

    create_database_sql = open(create_database_sql_dir + "create_database.sql", encoding='utf8').read() + '\n'
    create_whitelist_table_sql = open(create_database_sql_dir + "create_whitelist_table.sql",
                                      encoding='utf8').read() + '\n'

    create_whitelist_accumulative_table_sql = open(create_database_sql_dir + "create_whitelist_accumulative_table.sql",
                                                   encoding='utf8').read() + '\n'
    drop_whitelist_accumulative_table_sql = open(create_database_sql_dir + "drop_whitelist_accumulative_table.sql",
                                                 encoding='utf8').read() + '\n'
    create_covid_detection_table_sql = open(create_database_sql_dir + "create_covid_detection_table.sql",
                                            encoding='utf8').read() + '\n'
    drop_covid_detection_table_sql = open(create_database_sql_dir + "drop_covid_detection_table.sql",
                                          encoding='utf8').read() + '\n'
    create_cell_rules_table_sql = open(create_database_sql_dir + "create_cell_rules_table.sql",
                                       encoding='utf8').read() + '\n'
    drop_cell_rules_table_sql = open(create_database_sql_dir + "drop_cell_rules_table.sql",
                                     encoding='utf8').read() + '\n'
    create_gray_list_table_sql = open(create_database_sql_dir + "create_gray_list_table.sql",
                                      encoding='utf8').read() + '\n'
    drop_gray_list_table_sql = open(create_database_sql_dir + "drop_gray_list_table.sql",
                                    encoding='utf8').read() + '\n'

    try:
        connectionPool = getConnectionPool()
        conn = connectionPool.get_connection()
        cursor = conn.cursor()
        cursor.execute(create_database_sql)
        print('create database finished! time=', time.time() - start_time)
        print('create table whitelist finished! time=', time.time() - start_time)
        cursor.execute(drop_whitelist_accumulative_table_sql)
        cursor.execute(create_whitelist_accumulative_table_sql)
        print('create table accumulative whitelist finished! time=', time.time() - start_time)
        cursor.execute(drop_covid_detection_table_sql)
        cursor.execute(create_covid_detection_table_sql)
        print('create table covid_detection finished! time=', time.time() - start_time)
        cursor.execute(drop_cell_rules_table_sql)
        cursor.execute(create_cell_rules_table_sql)
        print('create table cell rules finished! time=', time.time() - start_time)
        cursor.execute(drop_gray_list_table_sql)
        cursor.execute(create_gray_list_table_sql)
        print('create table gray list finished! time=', time.time() - start_time)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    create_database()
