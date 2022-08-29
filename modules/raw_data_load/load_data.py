import os
import sys
import subprocess
import time
import pandas as pd
import numpy as np
import yaml
from yaml import SafeLoader

# add system path
sys.path.append(os.getcwd() + '/../..')
from modules.database.ConnectingPool import getConnectionPool

# global variables
config_filepath = '../../config.yaml'
load_covid_detection_sql_dir = 'load_covid_detection_sql/'
load_whitelist_sql_dir = 'load_whitelist_sql/'


def clean_data(x):
    """
    Several processes to clean data.
    (1) check null values; (2) remove newlines; (3) replace English commas; (4) check \ in values.
    :param x: An element of dataframe.
    :return: Cleaned element.
    """
    # check NULL values
    if pd.isnull(x):
        return '\\N'

    # remove newlines
    s = str(x)
    if s.find('\n') != -1:
        print(s)
        s = s.replace('\n', '')
        print(s)

    # replace English comma with Chinese comma
    s = s.replace(',', '，')

    # if s end with '\', add a blank after s
    if s.endswith('\\'):
        s = s + ' '

    return s


def load_whitelist(whitelist_input_filepath):
    """
    load whitelist into database.
    :param whitelist_input_filepath: Path of whitelist file, suppose the file is an Excel sheet.
    :return: None
    """

    start_time = time.time()
    print('start load raw whitelist to database...')

    # load config data
    system_configs, database_configs = None, None
    with open(config_filepath) as config_file:
        config_data = yaml.load(config_file, Loader=SafeLoader)
        database_configs = config_data['database']
        system_configs = config_data['system']

    # load initial data
    whitelist = pd.read_excel(whitelist_input_filepath, header=0)
    print('load raw whitelist finished! time=', time.time() - start_time)

    # clean data
    whitelist = whitelist.apply(np.vectorize(clean_data))
    print('clean data finished! time=', time.time() - start_time)

    # output file
    whitelist_out_file_name = 'whitelist.csv'
    whitelist.to_csv(whitelist_out_file_name, header=True, index=False, encoding='utf-8')
    print('output csv finished! time=', time.time() - start_time)

    # move covid detection records to mysql secure file path
    secure_file_path = database_configs['secure_file_priv']
    move_file_command = 'sudo -S cp whitelist.csv ' + secure_file_path
    subp = subprocess.Popen([move_file_command], shell=True, stdin=subprocess.PIPE)
    sudo_password = str.encode(system_configs['password'] + '\n')
    subp.communicate(sudo_password)
    print('move csv finished! time=', time.time() - start_time)

    # 1. load whitelist in csv file into a temporary table in database
    # 2. merge whitelist in temporary table into main whitelist table
    drop_table_sql = open(load_whitelist_sql_dir + 'drop_temporary_table.sql', encoding='utf8').read() + '\n'
    create_temporary_table_sql = open(load_whitelist_sql_dir + 'create_temporary_table.sql',
                                      encoding='utf8').read() + '\n'
    load_to_temporary_table_sql = open(load_whitelist_sql_dir + 'load_to_temporary_table.sql',
                                       encoding='utf8').read() + '\n'
    load_to_temporary_table_sql = load_to_temporary_table_sql.replace('secure_file_priv',
                                                                      database_configs['secure_file_priv'])
    remove_left_people_sql = open(load_whitelist_sql_dir + 'remove_left_people.sql', encoding='utf8').read() + '\n'
    add_coming_people_sql = open(load_whitelist_sql_dir + 'add_coming_people.sql', encoding='utf8').read() + '\n'

    connectionPool = getConnectionPool()
    conn = None
    cursor = None

    try:
        conn = connectionPool.get_connection()
        cursor = conn.cursor()
        cursor.execute(drop_table_sql)
        cursor.execute(create_temporary_table_sql)
        cursor.execute(load_to_temporary_table_sql)
        print('load whitelist into temporary table finished! time=', time.time() - start_time)
        cursor.execute(remove_left_people_sql)
        print('remove left people finished! time=', time.time() - start_time)
        cursor.execute(add_coming_people_sql)
        print('add newly coming people finished! time=', time.time() - start_time)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    print('load data into database finished! time=', time.time() - start_time)


def load_covid_detection(covid_detection_input_filepath):
    """
    load covid detection records into database.
    :param covid_detection_input_filepath: Path of covid detection record, suppose the file is an Excel sheet.
    :return:
    """

    start_time = time.time()
    print('start load raw covid detection records to database...')

    # load config data
    system_configs, database_configs = None, None
    with open(config_filepath) as config_file:
        config_data = yaml.load(config_file, Loader=SafeLoader)
        database_configs = config_data['database']
        system_configs = config_data['system']

    # load initial data
    covid_detection = pd.read_excel(covid_detection_input_filepath, header=0)
    print('load raw covid detection finished! time=', time.time() - start_time)

    # clean data
    covid_detection = covid_detection.apply(np.vectorize(clean_data))
    print('clean data finished! time=', time.time() - start_time)

    # output file
    covid_detection_out_file_name = 'covid_detection.csv'
    covid_detection.to_csv(covid_detection_out_file_name, header=True, index=False, encoding='utf-8')
    print('output csv finished! time=', time.time() - start_time)

    # move covid detection records to mysql secure file path
    secure_file_path = database_configs['secure_file_priv']
    move_file_command = 'sudo -S cp covid_detection.csv ' + secure_file_path
    subp = subprocess.Popen([move_file_command], shell=True, stdin=subprocess.PIPE)
    sudo_password = str.encode(system_configs['password'] + '\n')
    subp.communicate(sudo_password)
    print('move csv finished! time=', time.time() - start_time)

    # 1. load covid detection records in csv file into a temporary table in database
    # 2. merge records in temporary table into main covid detection records table
    drop_table_sql = open(load_covid_detection_sql_dir + 'drop_temporary_table.sql', encoding='utf8').read() + '\n'
    create_temporary_table_sql = open(load_covid_detection_sql_dir + 'create_temporary_table.sql',
                                      encoding='utf8').read() + '\n'
    load_to_temporary_table_sql = open(load_covid_detection_sql_dir + 'load_to_temporary_table.sql',
                                       encoding='utf8').read() + '\n'
    load_to_temporary_table_sql = load_to_temporary_table_sql.replace('secure_file_priv',
                                                                      database_configs['secure_file_priv'])
    update_modified_records_sql = open(load_covid_detection_sql_dir + 'update_modified_records.sql',
                                       encoding='utf8').read() + '\n'
    add_new_records_sql = open(load_covid_detection_sql_dir + 'add_new_records.sql', encoding='utf8').read() + '\n'

    connectionPool = getConnectionPool()
    conn = None
    cursor = None

    try:
        conn = connectionPool.get_connection()
        cursor = conn.cursor()
        cursor.execute(drop_table_sql)
        cursor.execute(create_temporary_table_sql)
        cursor.execute(load_to_temporary_table_sql)
        print('load data into temporary table finished! time=', time.time() - start_time)
        cursor.execute(update_modified_records_sql)
        print('update modified records finished! time=', time.time() - start_time)
        cursor.execute(add_new_records_sql)
        print('add new records finished! time=', time.time() - start_time)
        # cursor.execute(drop_table_sql)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    print('load data into database finished! time=', time.time() - start_time)


if __name__ == '__main__':
    whitelist_filepath = 'whitelist.xlsx'
    load_whitelist(whitelist_filepath)
    print('load whitelist finished!\n')

    covid_detection_filepath = 'covid_detection.xlsx'
    load_covid_detection(covid_detection_filepath)
    print('load covid detection finished!')
