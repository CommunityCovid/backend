import time
from modules.database.ConnectingPool import getConnectionPool

create_database_sql_dir = 'modules/database/database_creation_sql/'


def create_database(db):
    start_time = time.time()

    create_database_sql = open(create_database_sql_dir + "create_database.sql", encoding='utf8').read() + '\n'
    create_whitelist_table_sql = open(create_database_sql_dir + "create_whitelist_table.sql",
                                      encoding='utf8').read() + '\n'
    create_covid_detection_table_sql = open(create_database_sql_dir + "create_covid_detection_table_sql",
                                            encoding='utf8').read() + '\n'

    try:
        connectionPool = getConnectionPool()
        conn = connectionPool.get_connection()
        cursor = conn.cursor()
        cursor.execute(create_database_sql)
        print('create database finished! time=', time.time() - start_time)
        cursor.execute(create_whitelist_table_sql)
        print('create table whitelist finished! time=', time.time() - start_time)
        cursor.execute(create_covid_detection_table_sql)
        print('create table covid_detection finished! time=', time.time() - start_time)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
