import datetime
import os
import sys
import subprocess
import time
import pandas as pd
import numpy as np
import yaml
from tqdm import tqdm
from yaml import SafeLoader

# add system path
sys.path.append(os.getcwd() + '/../..')
from modules.database.ConnectingPool import getConnectionPool

# global variables
config_filepath = '../../config.yaml'
load_covid_detection_sql_dir = 'load_covid_detection_sql/'
load_whitelist_sql_dir = 'load_whitelist_sql/'
load_whitelist_accumulative_sql_dir = 'load_whitelist_accumulative_sql/'
load_gray_list_sql_dir = 'load_gray_list_sql/'
load_return_list_sql_dir = 'load_return_list_sql/'
load_grid_administrator_dir = 'load_grid_administrator_sql/'
load_cell_rules_dir = 'load_cell_rules_sql/'
analyze_data_sql_dir = 'analyze_data_sql/'


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


def load_whitelist(whitelist_input_filepath, whitelist_date):
    """
    load whitelist into database.
    :param whitelist_input_filepath: Path of whitelist file, suppose the file is an Excel sheet.
    :return: None
    """
    log = open('log/whitelist_log.txt', 'a')
    log.write("\n{}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    log.write("start load {}\n".format(whitelist_input_filepath))

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
    print('load raw whitelist finished! time =', time.time() - start_time)
    log.write('load raw whitelist finished! time = {}\n'.format(time.time() - start_time))

    # clean data
    whitelist = whitelist.apply(np.vectorize(clean_data))
    print('clean data finished! time =', time.time() - start_time)
    log.write('clean data finished! time = {}\n'.format(time.time() - start_time))

    # output file
    whitelist = whitelist[
        ['街道', '社区', '网格', '所居住花园小区/城中村名称', '所属电子哨兵卡口名称', '姓名', '性别', '人员类型', '证件类型', '证件号码', '出生年月', '手机号码', '国籍',
         '是否暂离', '户籍地址', '工作单位所在市', '工作单位所在行政区', '工作单位名称', '工作单位地址', '是否纳入市网格办统计', '楼栋地址', '楼栋编码', '房屋地址', '房屋编码', '备注',
         '审核结果', '审核人', '审核时间', '上报类型']]
    whitelist = whitelist[whitelist['是否暂离'].isin(['正常', '否'])]
    whitelist_out_file_name = 'whitelist.csv'
    whitelist.to_csv(whitelist_out_file_name, header=True, index=False, encoding='utf-8')
    print('output csv finished! time =', time.time() - start_time)
    log.write('output csv finished! time = {}\n'.format(time.time() - start_time))

    # move covid whitelist to mysql secure file path
    secure_file_path = database_configs['secure_file_priv']
    move_file_command = 'sudo -S cp whitelist.csv ' + secure_file_path
    subp = subprocess.Popen([move_file_command], shell=True, stdin=subprocess.PIPE)
    sudo_password = str.encode(system_configs['password'] + '\n')
    subp.communicate(sudo_password)
    print('move csv finished! time =', time.time() - start_time)
    log.write('move csv finished! time = {}\n'.format(time.time() - start_time))

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
    remove_left_people_sql = remove_left_people_sql.replace('{date}', whitelist_date)
    update_existing_people_sql = open(load_whitelist_sql_dir + 'update_existing_people.sql',
                                      encoding='utf8').read() + '\n'
    update_existing_people_sql = update_existing_people_sql.replace('{date}', whitelist_date)

    get_next_add_time_sql = "select min(加入白名单时间) from langxin_community.residents where 加入白名单时间 > '{date}'".replace(
        '{date}', whitelist_date)
    get_next_remove_time_sql = "select min(移出白名单时间) from langxin_community.residents where 移出白名单时间 > '{date}'".replace(
        '{date}', whitelist_date)
    add_coming_people_sql = open(load_whitelist_sql_dir + 'add_coming_people.sql', encoding='utf8').read() + '\n'
    add_coming_people_sql = add_coming_people_sql.replace('{date}', whitelist_date)

    connectionPool = getConnectionPool()
    conn = None
    cursor = None

    try:
        conn = connectionPool.get_connection()
        cursor = conn.cursor()
        cursor.execute(drop_table_sql)
        cursor.execute(create_temporary_table_sql)
        cursor.execute(load_to_temporary_table_sql)
        print('load whitelist into temporary table finished! time =', time.time() - start_time)
        log.write('load whitelist into temporary table finished! time = {}\n'.format(time.time() - start_time))
        cursor.execute(remove_left_people_sql)
        print('remove left people finished! time =', time.time() - start_time)
        log.write('remove left people finished! time = {}\n'.format(time.time() - start_time))
        cursor.execute(update_existing_people_sql)
        print('update existing people finished! time =', time.time() - start_time)
        log.write('update existing people finished! time = {}\n'.format(time.time() - start_time))

        remove_time = 'null'
        cursor.execute(get_next_add_time_sql)
        next_add_time = cursor.fetchone()[0]
        cursor.execute(get_next_remove_time_sql)
        next_remove_time = cursor.fetchone()[0]
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
        add_coming_people_sql = add_coming_people_sql.replace('{remove_time}', remove_time)
        cursor.execute(add_coming_people_sql)
        print('add newly coming people finished! time =', time.time() - start_time)
        log.write('add newly coming people finished! time = {}\n'.format(time.time() - start_time))
        cursor.execute(drop_table_sql)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    print('load data into database finished! time =', time.time() - start_time)
    log.write('load data into database finished! time = {}\n'.format(time.time() - start_time))


def load_whitelist_accumulative(whitelist_input_filepath, whitelist_date):
    """
    load whitelist into database.
    :param whitelist_date:
    :param whitelist_input_filepath: Path of whitelist file, suppose the file is an Excel sheet.
    :return: None
    """
    log = open('log/whitelist_accumulative_log.txt', 'a')
    log.write("\n{}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    log.write("start load {}\n".format(whitelist_input_filepath))

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
    print('load raw whitelist finished! time =', time.time() - start_time)
    log.write('load raw whitelist finished! time = {}\n'.format(time.time() - start_time))

    # clean data
    whitelist = whitelist.apply(np.vectorize(clean_data))
    print('clean data finished! time =', time.time() - start_time)
    log.write('clean data finished! time = {}\n'.format(time.time() - start_time))

    # output file
    whitelist = whitelist[
        ['街道', '社区', '网格', '所居住花园小区/城中村名称', '所属电子哨兵卡口名称', '姓名', '性别', '人员类型', '证件类型', '证件号码', '出生年月', '手机号码', '国籍',
         '是否暂离', '户籍地址', '工作单位所在市', '工作单位所在行政区', '工作单位名称', '工作单位地址', '是否纳入市网格办统计', '楼栋地址', '楼栋编码', '房屋地址', '房屋编码', '备注',
         '审核结果', '审核人', '审核时间', '上报类型']]
    whitelist = whitelist[whitelist['是否暂离'].isin(['正常', '否'])]
    whitelist_out_file_name = 'whitelist.csv'
    whitelist.to_csv(whitelist_out_file_name, header=True, index=False, encoding='utf-8')
    print('output csv finished! time =', time.time() - start_time)
    log.write('output csv finished! time = {}\n'.format(time.time() - start_time))

    # move whitelist to mysql secure file path
    secure_file_path = database_configs['secure_file_priv']
    move_file_command = 'sudo -S cp whitelist.csv ' + secure_file_path
    subp = subprocess.Popen([move_file_command], shell=True, stdin=subprocess.PIPE)
    sudo_password = str.encode(system_configs['password'] + '\n')
    subp.communicate(sudo_password)
    print('move csv finished! time =', time.time() - start_time)
    log.write('move csv finished! time = {}\n'.format(time.time() - start_time))

    # 1. load whitelist in csv file into a temporary table in database
    # 2. merge whitelist in temporary table into main whitelist table
    drop_table_sql = open(load_whitelist_accumulative_sql_dir + 'drop_temporary_table.sql',
                          encoding='utf8').read() + '\n'
    create_temporary_table_sql = open(load_whitelist_accumulative_sql_dir + 'create_temporary_table.sql',
                                      encoding='utf8').read() + '\n'
    load_to_temporary_table_sql = open(load_whitelist_accumulative_sql_dir + 'load_to_temporary_table.sql',
                                       encoding='utf8').read() + '\n'
    load_to_temporary_table_sql = load_to_temporary_table_sql.replace('secure_file_priv',
                                                                      database_configs['secure_file_priv'])
    remove_repeated_people_sql = open(load_whitelist_accumulative_sql_dir + 'remove_repeated_people.sql',
                                      encoding='utf8').read() + '\n'
    remove_repeated_people_sql = remove_repeated_people_sql.replace('{date}', whitelist_date)
    update_latest_sample_sql = open(load_whitelist_accumulative_sql_dir + 'update_latest_sample.sql',
                                    encoding='utf8').read() + '\n'
    update_latest_sample_sql = update_latest_sample_sql.replace('{date}', whitelist_date)
    split_cell_sql = open(load_whitelist_accumulative_sql_dir + 'split_cell_sql', encoding='utf8').read() + '\n'
    add_gray_list_not_related2age_sql = open(load_whitelist_accumulative_sql_dir + 'add_gray_list_not_related2age.sql',
                                             encoding='utf8').read() + '\n'
    add_gray_list_related2age_sql = open(load_whitelist_accumulative_sql_dir + 'add_gray_list_related2age.sql',
                                         encoding='utf8').read() + '\n'
    add_gray_list_related2age_sql = add_gray_list_related2age_sql.replace('{date}', whitelist_date)
    add_coming_people_sql = open(load_whitelist_accumulative_sql_dir + 'add_coming_people.sql',
                                 encoding='utf8').read() + '\n'
    add_coming_people_sql = add_coming_people_sql.replace('{date}', whitelist_date)

    connectionPool = getConnectionPool()

    try:
        conn = connectionPool.get_connection()
        cursor = conn.cursor()
        cursor.execute(drop_table_sql)
        cursor.execute(create_temporary_table_sql)
        cursor.execute(load_to_temporary_table_sql)
        print('load whitelist into temporary table finished! time =', time.time() - start_time)
        log.write('load whitelist into temporary table finished! time = {}\n'.format(time.time() - start_time))
        cursor.execute(remove_repeated_people_sql)
        print('remove repeated people in temporary table finished! time =', time.time() - start_time)
        log.write('remove repeated people in temporary table finished! time = {}\n'.format(time.time() - start_time))
        cursor.execute(update_latest_sample_sql)
        print('compute latest sample time finished! time =', time.time() - start_time)
        log.write('compute latest sample time finished! time = {}\n'.format(time.time() - start_time))
        cursor.execute(split_cell_sql)
        print('split cell finished! time =', time.time() - start_time)
        log.write('split cell finished! time = {}\n'.format(time.time() - start_time))
        cursor.execute(add_gray_list_not_related2age_sql)
        cursor.execute(add_gray_list_related2age_sql)
        print('update gray list finished! time =', time.time() - start_time)
        log.write('update gray list finished! time = {}\n'.format(time.time() - start_time))
        cursor.execute(add_coming_people_sql)
        print('add newly coming people finished! time =', time.time() - start_time)
        log.write('add newly coming people finished! time = {}\n'.format(time.time() - start_time))
        cursor.execute(drop_table_sql)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    print('load data into database finished! time =', time.time() - start_time)
    log.write('load data into database finished! time = {}\n'.format(time.time() - start_time))


def process_raw_gray_list(gray_list):
    """

    :param gray_list:
    :return:
    """
    gray_list_classes_kinds = ['I类灰名单（不方便采样核酸人员）', 'II类灰名单（不配合采样核酸人员）']
    gray_list_reasons_kinds = ['2岁及以下婴幼儿', '80岁及以上老人', '精神障碍患者',
                               '行动不便（含残障人士、孕妇、坐月子等不便于外出采样情况）', '不便于采样的其他短期疾病（如口腔疾病等）',
                               '备注', '极不配合、强烈抵触采样', '7天以上无核酸采样记录', '周末返回石岩但不配合采样人员',
                               '已采样但拒绝提供石岩外采样凭据', '备注']

    # omit children and the aged, process these people in sql
    column_classes_start_offset = 9
    column_second_class_start_offset = 15
    column_classes_end_offset = 20
    gray_list_classes, gray_list_reasons = [], []

    for index, row in gray_list.iterrows():
        find = False
        for i in range(column_classes_start_offset, column_classes_end_offset):
            if not pd.isnull(row[i]):
                find = True
                gray_list_classes.append(2 - int(i < column_second_class_start_offset))
                gray_list_reasons.append(gray_list_reasons_kinds[i - column_classes_start_offset])
                break
        if not find:
            gray_list_classes.append(0)
            gray_list_reasons.append('')

    # cat id column
    new_gray_list = gray_list.iloc[:, :9]

    # append classes and reasons of gray list
    new_gray_list.insert(len(new_gray_list.columns), '灰名单类型', gray_list_classes)
    new_gray_list.insert(len(new_gray_list.columns), '灰名单原因', gray_list_reasons)

    # remove people which is not in gray list
    new_gray_list = new_gray_list[new_gray_list.灰名单类型 != 0]

    # remove people which age less than 3 and larger than 79.
    new_gray_list = new_gray_list[new_gray_list.灰名单原因 != '2岁及以下婴幼儿']
    new_gray_list = new_gray_list[new_gray_list.灰名单原因 != '80岁及以上老人']

    # format the column names
    new_gray_list.columns = ['社区', '网格', '姓名', '证件号', '联系电话', '出生日期', '年龄', '房屋编码', '房屋地址',
                             '灰名单类型', '灰名单原因']

    new_gray_list = new_gray_list[['姓名', '证件号', '灰名单类型', '灰名单原因']]

    return new_gray_list


def load_gray_list(gray_list_input_filepath):
    """
    load gray list into database.
    :param gray_list_input_filepath:
    :return:
    """
    log = open('log/gray_list_log.txt', 'a')
    log.write("\n{}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    log.write("start load {}\n".format(gray_list_input_filepath))

    start_time = time.time()
    print('start load raw gray list to database...')

    # load config data
    system_configs, database_configs = None, None
    with open(config_filepath) as config_file:
        config_data = yaml.load(config_file, Loader=SafeLoader)
        database_configs = config_data['database']
        system_configs = config_data['system']

    # load initial data
    gray_list = pd.read_excel(gray_list_input_filepath, header=None).loc[4:]

    # process raw gray list
    gray_list = process_raw_gray_list(gray_list)

    # clean data
    gray_list = gray_list.apply(np.vectorize(clean_data))
    print('clean data finished! time =', time.time() - start_time)
    log.write('clean data finished! time = {}\n'.format(time.time() - start_time))

    # output file
    gray_list_out_file_name = 'gray_list.csv'
    gray_list.to_csv(gray_list_out_file_name, header=True, index=False, encoding='utf-8')

    # move covid detection records to mysql secure file path
    secure_file_path = database_configs['secure_file_priv']
    move_file_command = 'sudo -S cp gray_list.csv ' + secure_file_path
    subp = subprocess.Popen([move_file_command], shell=True, stdin=subprocess.PIPE)
    sudo_password = str.encode(system_configs['password'] + '\n')
    subp.communicate(sudo_password)
    print('move csv finished! time =', time.time() - start_time)
    log.write('move csv finished! time = {}\n'.format(time.time() - start_time))

    # 1. load gray list in csv file into temporary table in database
    # 2. merge gray list in temporary table into main whitelist table
    drop_table_sql = open(load_gray_list_sql_dir + 'drop_temporary_table.sql', encoding='utf8').read() + '\n'
    create_temporary_table_sql = open(load_gray_list_sql_dir + 'create_temporary_table.sql',
                                      encoding='utf8').read() + '\n'
    load_to_temporary_table_sql = open(load_gray_list_sql_dir + 'load_to_temporary_table.sql',
                                       encoding='utf8').read() + '\n'
    load_to_temporary_table_sql = load_to_temporary_table_sql.replace('secure_file_priv',
                                                                      database_configs['secure_file_priv'])
    remove_all_gray_list_sql = open(load_gray_list_sql_dir + 'remove_all_gray_list.sql').read() + '\n'
    add_gray_list_not_related2age_sql = open(load_gray_list_sql_dir + 'add_gray_list_not_related2age.sql').read() + '\n'
    add_gray_list_related2age_sql = open(load_gray_list_sql_dir + 'add_gray_list_related2age.sql').read() + '\n'

    connectionPool = getConnectionPool()
    conn = None
    cursor = None

    try:
        conn = connectionPool.get_connection()
        cursor = conn.cursor()
        # cursor.execute(drop_table_sql)
        # cursor.execute(create_temporary_table_sql)
        # cursor.execute(load_to_temporary_table_sql)
        print('load data into temporary table finished! time =', time.time() - start_time)
        log.write('load data into temporary table finished! time = {}\n'.format(time.time() - start_time))

        cursor.execute(remove_all_gray_list_sql)
        cursor.execute(add_gray_list_not_related2age_sql)
        cursor.execute(add_gray_list_related2age_sql)
        print('update gray list finished! time =', time.time() - start_time)
        log.write('update gray list finished! time = {}\n'.format(time.time() - start_time))
        # cursor.execute(drop_table_sql)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

    print('load data into database finished! time =', time.time() - start_time)
    log.write('load data into database finished! time = {}\n'.format(time.time() - start_time))


def load_covid_detection(covid_detection_input_filepath):
    """
    load covid detection records into database.
    :param covid_detection_input_filepath: Path of covid detection record, suppose the file is an Excel sheet.
    :return:
    """
    log = open('log/covid_detection_log.txt', 'a')
    log.write("\n{}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    log.write("start load {}\n".format(covid_detection_input_filepath))

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
    print('load raw covid detection finished! time = {}'.format(time.time() - start_time))
    log.write('load raw covid detection finished! time = {}\n'.format(time.time() - start_time))

    # clean data
    covid_detection = covid_detection.apply(np.vectorize(clean_data))
    print('clean data finished! time = {}'.format(time.time() - start_time))
    log.write('clean data finished! time = {}\n'.format(time.time() - start_time))

    # output file
    covid_detection = covid_detection[
        ['姓名', '出生日期', '年龄', '电话号码', '机构所在地', '采样机构', '采样时间', '检测机构', '检测时间', '检测结果', '检测结果填报时间', '复核结果', '复核机构',
         '复核时间', '性别', '国家/地区', '居住地', '证件类型', '证件号码', '未提供有效证件原因', '检测人群分类', '应检尽检类别', '导入机构', '样本条形码', '样本类型', '检测项目',
         '采样点行政区划', '采样地点', '所在学校/单位名称', '备注1', '备注2', '采集类型', '导入时间', '创建人账号', '创建人姓名']]
    covid_detection_out_file_name = 'covid_detection.csv'
    covid_detection.to_csv(covid_detection_out_file_name, header=True, index=False, encoding='utf-8')
    print('output csv finished! time =', time.time() - start_time)
    log.write('output csv finished! time = {}\n'.format(time.time() - start_time))

    # move covid detection records to mysql secure file path
    secure_file_path = database_configs['secure_file_priv']
    move_file_command = 'sudo -S cp covid_detection.csv ' + secure_file_path
    subp = subprocess.Popen([move_file_command], shell=True, stdin=subprocess.PIPE)
    sudo_password = str.encode(system_configs['password'] + '\n')
    subp.communicate(sudo_password)
    print('move csv finished! time =', time.time() - start_time)
    log.write('move csv finished! time = {}\n'.format(time.time() - start_time))

    # 1. load covid detection records in csv file into a temporary table in database
    # 2. merge records in temporary table into main covid detection records table
    drop_table_sql = open(load_covid_detection_sql_dir + 'drop_temporary_table.sql', encoding='utf8').read() + '\n'
    create_temporary_table_sql = open(load_covid_detection_sql_dir + 'create_temporary_table.sql',
                                      encoding='utf8').read() + '\n'
    load_to_temporary_table_sql = open(load_covid_detection_sql_dir + 'load_to_temporary_table.sql',
                                       encoding='utf8').read() + '\n'
    load_to_temporary_table_sql = load_to_temporary_table_sql.replace('secure_file_priv',
                                                                      database_configs['secure_file_priv'])
    # update_modified_records_sql = open(load_covid_detection_sql_dir + 'update_modified_records.sql',
    #                                    encoding='utf8').read() + '\n'
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
        print('load data into temporary table finished! time =', time.time() - start_time)
        log.write('load data into temporary table finished! time = {}\n'.format(time.time() - start_time))

        cursor.execute(add_new_records_sql)
        print('add new records finished! time =', time.time() - start_time)
        log.write('add new records finished! time = {}\n'.format(time.time() - start_time))
        cursor.execute(drop_table_sql)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    print('load data into database finished! time =', time.time() - start_time)
    log.write('load data into database finished! time = {}\n'.format(time.time() - start_time))
    log.close()


def load_return_list(return_list_input_filepath, return_list_date):
    log = open('log/return_list_log.txt', 'a')
    log.write("\n{}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    log.write("start load {}\n".format(return_list_input_filepath))

    start_time = time.time()
    print('start load raw return list records to database...')

    # load config data
    system_configs, database_configs = None, None
    with open(config_filepath) as config_file:
        config_data = yaml.load(config_file, Loader=SafeLoader)
        database_configs = config_data['database']
        system_configs = config_data['system']

    # load initial data
    return_list = pd.read_excel(return_list_input_filepath, header=0)
    print('load raw return finished! time =', time.time() - start_time)
    log.write('load raw return finished! time = {}\n'.format(time.time() - start_time))

    # selected needed columns and set column names
    return_list = return_list.iloc[:, :10]
    return_list.columns = ['社区', '人员类型', '分类', '网格', '姓名', '证件号码', '手机号码', '房屋地址', '最近采样时间', '楼栋编码']

    # clean data
    return_list = return_list.apply(np.vectorize(clean_data))
    print('clean data finished! time =', time.time() - start_time)
    log.write('clean data finished! time = {}\n'.format(time.time() - start_time))

    # output file
    return_list_out_file_name = 'return_list.csv'
    return_list.to_csv(return_list_out_file_name, header=True, index=False, encoding='utf-8')
    print('output csv finished! time =', time.time() - start_time)
    log.write('output csv finished! time = {}\n'.format(time.time() - start_time))

    # move covid detection records to mysql secure file path
    secure_file_path = database_configs['secure_file_priv']
    move_file_command = 'sudo -S cp return_list.csv ' + secure_file_path
    subp = subprocess.Popen([move_file_command], shell=True, stdin=subprocess.PIPE)
    sudo_password = str.encode(system_configs['password'] + '\n')
    subp.communicate(sudo_password)
    print('move csv finished! time =', time.time() - start_time)
    log.write('move csv finished! time = {}\n'.format(time.time() - start_time))

    # 1. load return list in csv file into a temporary table in database
    # 2. add returned records to main covid detection records table
    drop_table_sql = open(load_return_list_sql_dir + 'drop_temporary_table.sql', encoding='utf8').read() + '\n'
    create_temporary_table_sql = open(load_return_list_sql_dir + 'create_temporary_table.sql',
                                      encoding='utf8').read() + '\n'
    load_to_temporary_table_sql = open(load_return_list_sql_dir + 'load_to_temporary_table.sql',
                                       encoding='utf8').read() + '\n'
    load_to_temporary_table_sql = load_to_temporary_table_sql.replace('secure_file_priv',
                                                                      database_configs['secure_file_priv'])
    add_return_list_sql = open(load_return_list_sql_dir + 'add_return_list.sql', encoding='utf8').read() + '\n'
    add_return_list_sql = add_return_list_sql.replace('{date}', return_list_date)

    connectionPool = getConnectionPool()
    conn = None
    cursor = None

    try:
        conn = connectionPool.get_connection()
        cursor = conn.cursor()
        cursor.execute(drop_table_sql)
        cursor.execute(create_temporary_table_sql)
        cursor.execute(load_to_temporary_table_sql)
        print('load data into temporary table finished! time =', time.time() - start_time)
        log.write('load data into temporary table finished! time = {}\n'.format(time.time() - start_time))
        cursor.execute(add_return_list_sql)
        print('add return list to covid detection records finished! time =', time.time() - start_time)
        log.write('add return list to covid detection records finished! time = {}\n'.format(time.time() - start_time))
        cursor.execute(drop_table_sql)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    print('load data into database finished! time =', time.time() - start_time)
    log.write('load data into database finished! time = {}\n'.format(time.time() - start_time))


def load_grid_administrator(grid_administrator_input_filepath):
    log = open('log/grid_administrator_log.txt', 'a')
    log.write("\n{}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    log.write("start load {}\n".format(grid_administrator_input_filepath))

    start_time = time.time()
    print('start load grid administrator...')

    # load initial data
    grid_administrator = pd.read_excel(grid_administrator_input_filepath, header=0)
    print('load raw grid administrator finished! time =', time.time() - start_time)
    log.write('load raw grid administrator finished! time = {}\n'.format(time.time() - start_time))

    # clean data
    grid_administrator = grid_administrator.apply(np.vectorize(clean_data))
    print('clean data finished! time =', time.time() - start_time)
    log.write('clean data finished! time = {}\n'.format(time.time() - start_time))

    # cat grid administrators info pairs
    values_str = ' '
    for i in range(grid_administrator.shape[0]):
        values_str += "('{}', '{}'), ".format(grid_administrator['网格号'][i], grid_administrator['姓名'][i])
    values_str = values_str.strip(', ')

    # place grid administrators info into sql and execute straightly
    drop_table_sql = open(load_grid_administrator_dir + 'drop_table.sql', encoding='utf8').read() + '\n'
    create_table_sql = open(load_grid_administrator_dir + 'create_table.sql', encoding='utf8').read() + '\n'
    add_grid_administrators_sql = open(load_grid_administrator_dir + 'add_grid_administrators.sql',
                                       encoding='utf8').read().replace('{values}', values_str) + '\n'

    connectionPool = getConnectionPool()

    try:
        conn = connectionPool.get_connection()
        cursor = conn.cursor()
        cursor.execute(drop_table_sql)
        cursor.execute(create_table_sql)
        cursor.execute(add_grid_administrators_sql)
        print('load grid administrators info finished! time =', time.time() - start_time)
        log.write('load grid administrators info finished! time = {}\n'.format(time.time() - start_time))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    print('load data into database finished! time =', time.time() - start_time)
    log.write('load data into database finished! time = {}\n'.format(time.time() - start_time))


def load_cell_rules(cell_rules_input_filepath):
    log = open('log/cell_rules_log.txt', 'a')
    log.write("\n{}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    log.write("start load {}\n".format(cell_rules_input_filepath))

    start_time = time.time()

    # load initial data
    cell_rules = pd.read_excel(cell_rules_input_filepath, header=0)
    print('load raw cell rules finished! time =', time.time() - start_time)
    log.write('load raw cell rules finished! time = {}\n'.format(time.time() - start_time))

    # selected needed columns and set column names
    cell_rules = cell_rules[['楼栋地址', '所属小区']]

    # clean data
    cell_rules = cell_rules.apply(np.vectorize(clean_data))
    print('clean data finished! time =', time.time() - start_time)
    log.write('clean data finished! time = {}\n'.format(time.time() - start_time))

    # cat cell rules info pairs
    values_str = ' '
    for i in range(cell_rules.shape[0]):
        values_str += "('{}', '{}'), ".format(cell_rules['楼栋地址'][i], cell_rules['所属小区'][i])
    values_str = values_str.strip(', ')

    # place cell rules info into sql and execute straightly
    drop_table_sql = open(load_cell_rules_dir + 'drop_table.sql', encoding='utf8').read() + '\n'
    create_table_sql = open(load_cell_rules_dir + 'create_table.sql', encoding='utf8').read() + '\n'
    add_cell_rules_sql = open(load_cell_rules_dir + 'add_cell_rules.sql',
                              encoding='utf8').read().replace('{values}', values_str) + '\n'

    connectionPool = getConnectionPool()

    try:
        conn = connectionPool.get_connection()
        cursor = conn.cursor()
        cursor.execute(drop_table_sql)
        cursor.execute(create_table_sql)
        cursor.execute(add_cell_rules_sql)
        print('load cell rules finished! time =', time.time() - start_time)
        log.write('load cell rules finished! time = {}\n'.format(time.time() - start_time))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    print('load data into database finished! time =', time.time() - start_time)
    log.write('load data into database finished! time = {}\n'.format(time.time() - start_time))


def split_cell(location_cell_input_filepath):
    log = open('log/split_cell_log.txt', 'a')
    log.write("\n{}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    log.write("start load {}\n".format(location_cell_input_filepath))

    start_time = time.time()

    # load initial data
    location_cell = pd.read_excel(location_cell_input_filepath, header=0)
    print('load raw cell data finished! time =', time.time() - start_time)
    log.write('load raw cell data finished! time = {}\n'.format(time.time() - start_time))

    # selected needed columns and set column names
    location_cell = location_cell[['楼栋地址', '所属小区']]

    # clean data
    location_cell = location_cell.apply(np.vectorize(clean_data))
    print('clean data finished! time =', time.time() - start_time)
    log.write('clean data finished! time = {}\n'.format(time.time() - start_time))

    # get cells list
    cells = pd.unique(location_cell['所属小区'])

    # split locations into corresponding cell
    cell_location_dic = {}
    for cell in cells:
        cell_location_dic[cell] = []
    for index, row in location_cell.iterrows():
        cell_location_dic[row['所属小区']].append(row['楼栋地址'])

    # create SQLs to split cell
    split_cell_sqls = []
    for cell in cells:
        locations = cell_location_dic[cell]
        if len(locations) > 0:
            sql = "update langxin_community.residents_accumulative set 小区 = " \
                  "'{}' where 房屋地址 like '%{}%' and 小区 is null".format(cell, locations[0])
            for i in range(1, len(locations)):
                sql += " or 房屋地址 like '%{}%'".format(locations[i])
            sql += ';\n'
            split_cell_sqls.append(sql)

    try:
        connectionPool = getConnectionPool()
        conn = connectionPool.get_connection()
        cursor = conn.cursor()

        for i in tqdm(range(len(split_cell_sqls))):
            sql = split_cell_sqls[i]
            cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

    print('split cell finished! time =', time.time() - start_time)
    log.write('split cell finished! time = {}\n'.format(time.time() - start_time))


def analyze_data():
    log = open('log/analyze_log.txt', 'a')
    log.write("\n{}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    start_time = time.time()
    print('start analyze newly imported data...')

    # obtain a connection pool
    connectionPool = getConnectionPool()
    conn = None
    cursor = None

    # 1. compute latest sample time into whitelist
    compute_latest_sample_sql = open(analyze_data_sql_dir + 'update_latest_sample_accumulative.sql',
                                     encoding='utf8').read() + '\n'

    try:
        conn = connectionPool.get_connection()
        cursor = conn.cursor()
        cursor.execute(compute_latest_sample_sql)
        conn.commit()
        print('compute latest sampling time finished! time =', time.time() - start_time)
        log.write('compute latest sampling time finished! time = {}\n'.format(time.time() - start_time))
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    print('analyze data finished! time =', time.time() - start_time)
    log.write('analyze data finished! time = {}\n'.format(time.time() - start_time))


if __name__ == '__main__':
    whitelist_dir = 'raw_data/白名单/'
    whitelist_filenames = ['2022-07-27_浪心白名单.xlsx', '2022-08-19_浪心白名单.xlsx', '2022-08-24_浪心白名单.xlsx',
                           '2022-08-25_浪心白名单.xlsx', '2022-09-08_白名单.xlsx', '2022-09-09_白名单.xlsx',
                           '2022-09-13_白名单.xlsx', '2022-09-14_白名单.xlsx', '2022-09-15_白名单.xlsx',
                           '2022-09-16_白名单.xlsx', '2022-09-18_白名单.xlsx', '2022-09-19_白名单.xlsx',
                           '2022-09-20_白名单.xlsx']
    whitelist_right_order = [i for i in range(len(whitelist_filenames))]
    whitelist_inverse_order = whitelist_right_order[::-1]
    whitelist_random_order = [0, 4, 11, 3, 9, 2, 6, 12, 7, 1, 10, 5, 8]

    covid_detection_dir = 'raw_data/核酸/'
    covid_detection_filenames = ['2022-09-08_核酸.xlsx', '2022-09-09_核酸.xlsx', '2022-09-10_核酸.xlsx',
                                 '2022-09-11_核酸.xlsx', '2022-09-12_核酸.xlsx', '2022-09-13_核酸.xlsx',
                                 '2022-09-14_核酸.xlsx', '2022-09-15_核酸.xlsx', '2022-09-16_核酸.xlsx',
                                 '2022-09-17_核酸.xlsx', '2022-09-18_核酸.xlsx', '2022-09-19_核酸.xlsx',
                                 '2022-09-20_核酸.xlsx']
    covid_detection_right_order = [i for i in range(len(covid_detection_filenames))]
    covid_detection_inverse_order = covid_detection_right_order[::-1]
    covid_detection_random_order = [0, 4, 11, 3, 9, 2, 6, 12, 7, 1, 10, 5, 8]

    # for i in whitelist_random_order:
    #     whitelist_date = whitelist_filenames[i].split('_')[0]
    #     whitelist_filepath = whitelist_dir + whitelist_filenames[i]
    #     print("\nloading", whitelist_filepath)
    #     load_whitelist(whitelist_filepath, whitelist_date)
    # print('load whitelist finished!\n')

    for i in [12]:
        whitelist_date = whitelist_filenames[i].split('_')[0]
        whitelist_filepath = whitelist_dir + whitelist_filenames[i]
        print("\nloading", whitelist_filepath)
        load_whitelist_accumulative(whitelist_filepath, whitelist_date)
    print('load whitelist finished!\n')

    # for i in covid_detection_random_order:
    #     covid_detection_filepath = covid_detection_dir + covid_detection_filenames[i]
    #     print("\nloading", covid_detection_filepath)
    #     load_covid_detection(covid_detection_filepath)
    # print('load covid detection finished!\n')

    # gray_list_filepath = 'raw_data/gray_list.xlsx'
    # load_gray_list(gray_list_filepath)
    # print('load gray list finished!')

    # return_list_filepath = 'return_list.xlsx'
    # load_return_list(return_list_filepath, '2022-08-25')
    # print('load return list finished!')

    # grid_administrator_filepath = 'raw_data/grid_administrators.xlsx'
    # load_grid_administrator(grid_administrator_filepath)
    # print('load grid administrator finished!')

    # location_cell_filepath = 'raw_data/cell.xlsx'
    # split_cell(location_cell_filepath)

    # cell_rules_filepath = 'raw_data/cell.xlsx'
    # load_cell_rules(cell_rules_filepath)

    # analyze_data()
    # print('analyze newly imported data finished!')