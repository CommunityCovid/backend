import datetime
import logging
import re
import string
import subprocess
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask import render_template, Response, json, make_response
import os

from utils.util import *
from utils.dao import *
from utils.dao2 import *

from modules.raw_data_load.load_data import *

from utils.statics import *
from flask_mysqldb import MySQL

FILE_ABS_PATH = os.path.dirname(__file__)
DATA_DIR = os.path.join(FILE_ABS_PATH, 'data')

app = Flask(__name__)
CORS(app)

db_server = None

config_filepath = 'config.yaml'
with open(config_filepath) as config_file:
    config_data = yaml.load(config_file, Loader=SafeLoader)
    database_configs = config_data['database']
    app.config['MYSQL_USER'] = database_configs['user']
    app.config['MYSQL_PASSWORD'] = database_configs['password']
    app.config['MYSQL_HOST'] = database_configs['host']
    app.config['MYSQL_DB'] = database_configs['database']
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

db = MySQL(app)


# logging.basicConfig(level=logging.DEBUG  # 设置日志输出格式
#                     , filename="./data/server.log"  # log日志输出的文件位置和文件名
#                     , format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s"
#                     # 日志输出的格式
#                     # -8表示占位符，让输出左对齐，输出长度都为8位
#                     , datefmt="%Y-%m-%d %H:%M:%S"  # 时间输出的格式
#                     )


@app.route('/api/getCommunityCnt', methods=['POST', 'GET'])
def get_community_cnt():
    params = request.json
    date = params['date']
    record_limit = params["recordLimit"]
    date_tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
    date_next = date_tmp + datetime.timedelta(days=1)
    date_record = date_tmp - datetime.timedelta(days=record_limit)
    total_cnt = get_whitelist_num(db, date, date_next)
    finished_cnt = get_finished_num(db, date, record_limit)
    return jsonify(
        {"totalCount": int(total_cnt),
         "finishedCnt": int(finished_cnt)
         }), 200, {"Content-Type": "application/json"}


@app.route('/api/getCommunityGreyCnt', methods=['POST', 'GET'])
def get_community_grey_cnt():
    params = request.json
    date = params['date']
    record_limit = params["recordLimit"]
    date_tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
    date_next = date_tmp + datetime.timedelta(days=1)
    date_record = date_tmp - datetime.timedelta(days=record_limit)

    total_cnt = get_greylist_num(db, date, date_next)
    finished_cnt = get_finished_grey_num(db, date,record_limit)

    return jsonify(
        {"totalCount": int(total_cnt),
         "finishedCnt": int(finished_cnt)
         }), 200, {"Content-Type": "application/json"}


@app.route('/api/getGridsCnt', methods=['POST', 'GET'])
def get_grids_cnt():
    params = request.json
    date = params["date"]
    record_limit = params["recordLimit"]
    date_tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
    date_next = date_tmp + datetime.timedelta(days=1)
    date_record = date_tmp - datetime.timedelta(days=record_limit)
    grids_total_cnt = get_grid_whitelist(db, date)
    grid_finish_cnt = get_grid_finished(db, date, record_limit)

    grid_info_map = {}
    for item in grids_total_cnt:
        grid_info_map.update({
            item["网格"]: {"totalCnt": item["cnt"],
                         "finishedCnt": 0}
        })
    for item in grid_finish_cnt:
        grid_info_map[item["网格"]].update({
            "finishedCnt": item["cnt"]
        })
    return jsonify(grid_info_map, 200, {"Content-Type": "application/json"})


@app.route('/api/getGridsGreyCnt', methods=['POST', 'GET'])
def get_grids_grey_cnt():
    params = request.json
    date = params["date"]
    record_limit = params["recordLimit"]
    date_tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
    date_next = date_tmp + datetime.timedelta(days=1)
    date_record = date_tmp - datetime.timedelta(days=record_limit)
    grids_total_cnt = get_grid_grey_whitelist(db, date)
    grid_finish_cnt = get_grid_grey_finished(db, date, record_limit)

    grid_info_map = {}
    for item in grids_total_cnt:
        grid_info_map.update({
            item["网格"]: {"totalCnt": item["cnt"],
                         "finishedCnt": 0}
        })
    for item in grid_finish_cnt:
        grid_info_map[item["网格"]].update({
            "finishedCnt": item["cnt"]
        })
    return jsonify(grid_info_map, 200, {"Content-Type": "application/json"})


@app.route('/api/getGridCnt', methods=['POST', 'GET'])
def get_grid_cnt():
    params = request.json
    date = params["date"]
    record_limit = params["recordLimit"]
    grid_name = params["grid"]
    date_tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
    date_next = date_tmp + datetime.timedelta(days=1)
    date_record = date_tmp - datetime.timedelta(days=int(record_limit))
    grids_total_cnt = get_grid_whitelist(db, date)
    grid_finish_cnt = get_grid_finished(db, date, int(record_limit))

    total_cnt, finished_cnt = 0, 0

    for item in grids_total_cnt:
        if item["网格"] == grid_name:
            total_cnt = item["cnt"]
            break
    for item in grid_finish_cnt:
        if item["网格"] == grid_name:
            finished_cnt = item["cnt"]
            break

    return jsonify({"totalCnt": total_cnt, "finishedCnt": finished_cnt}, 200, {"Content-Type": "application/json"})


@app.route('/api/getGridGreyCnt', methods=['POST', 'GET'])
def get_grid_grey_cnt():
    params = request.json
    date = params["date"]
    record_limit = params["recordLimit"]
    grid_name = params["grid"]
    date_tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
    date_next = date_tmp + datetime.timedelta(days=1)
    date_record = date_tmp - datetime.timedelta(days=int(record_limit))
    grids_total_cnt = get_grid_grey_whitelist(db, date)
    grid_finish_cnt = get_grid_grey_finished(db, date, int(record_limit))

    total_cnt, finished_cnt = 0, 0

    for item in grids_total_cnt:
        if item["网格"] == grid_name:
            total_cnt = item["cnt"]
            break
    for item in grid_finish_cnt:
        if item["网格"] == grid_name:
            finished_cnt = item["cnt"]
            break

    return jsonify({"totalCnt": total_cnt, "finishedCnt": finished_cnt}, 200, {"Content-Type": "application/json"})


@app.route('/api/getCommunityPeople', methods=['POST', 'GET'])
def get_whitelist():
    whitelist = get_whitelist()
    values = []
    for item in whitelist:
        values.append([item[key] for key in residents_columns])
    return jsonify({"columns": residents_columns, "people": values}, 200, {"Content-Type": "application/json"})


@app.route('/api/getGreyListPeople', methods=['POST', 'GET'])
def get_grey_list_people():
    params = request.json
    date = params["date"]
    grey_list = get_grey_list(db=db, date=date)

    values = []
    for item in grey_list:
        values.append([item[key] for key in residents_columns])
    return jsonify({"columns": residents_columns, "people": values}, 200, {"Content-Type": "application/json"})


@app.route('/api/getGridPeople', methods=['POST', 'GET'])
def get_grid_people():
    params = request.json
    grid = params["grid"]
    date = params["date"]
    date_tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
    whitelist = get_grid_whitelist_people(db, date, grid)
    values = []
    for item in whitelist:
        values.append([item[key] for key in residents_columns])
    return jsonify({"columns": residents_columns, "people": values}, 200, {"Content-Type": "application/json"})


@app.route('/api/getGridGreyPeople', methods=['POST', 'GET'])
def get_grid_grey_people():
    params = request.json
    grid = params["grid"]
    date = params["date"]
    date_tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
    whitelist = get_grid_greylist_people(db, date, grid)
    values = []
    for item in whitelist:
        values.append([item[key] for key in residents_columns])
    return jsonify({"columns": residents_columns, "people": values}, 200, {"Content-Type": "application/json"})


@app.route('/api/uploadFile', methods=['POST', 'GET'])
def upload_file():
    file = request.files.get("file")
    file_name = request.form.get("name")
    if not os.path.exists('data'):
        os.mkdir('data')
    file.save(f"data/{file_name}")
    date = file_name.split("_")[0]
    if "白名单" in file_name:
        load_whitelist_accumulative(f"data/{file_name}", date, db)
    elif "核酸" in file_name:
        load_covid_detection(f"data/{file_name}", date, db)
    elif "灰名单" in file_name:
        load_gray_list(f"data/{file_name}", db)
    elif "小区" in file_name:
        load_cell_rules(f"data/{file_name}", db)
    elif "网格" in file_name:
        load_grid_administrator(f"data/{file_name}", db)
    # elif "回流数据" in file_name:
    #     load_return_list(f"data/{file_name}", date, db)
    #     analyze_data(db)

    # logging.info(f"receive and store file {file_name} in './data'")
    return jsonify({}, 200, {"Content-Type": "application/json"})


@app.route('/api/getRecords', methods=['POST', 'GET'])
def get_records():
    params = request.json
    date = params["date"]
    date_tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
    date_next = date_tmp + datetime.timedelta(days=1)
    data = get_records_position(db, date, date_next)
    position = []
    timesMap = {}
    for item in data:
        p = item["采样地点"]
        p = p.strip(string.ascii_uppercase).strip(string.digits)
        p = p.strip("浪心")
        # p = p.strip(string.digits)
        if p not in timesMap:
            timesMap[p] = []
            position.append(p)
        timesMap[p].append(int(item["采样时间"].hour))
    res = {}
    position.sort()
    for p in position:
        times = timesMap[p]
        res[p] = {}
        for i in range(24):
            res[p][i] = 0
        for t in times:
            res[p][t] += 1
    return jsonify({"heatMap": res, "position": position}, 200, {"Content-Type": "application/json"})


@app.route('/api/getGridsTimeInfo', methods=['POST', 'GET'])
def get_grids_time_info():
    params = request.json
    date = params["date"]
    limit_record = params["recordLimit"]
    date_tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
    date_next = date_tmp + datetime.timedelta(days=1)
    record_limit = date_tmp - datetime.timedelta(days=limit_record)
    data = get_grids_record_time(db, date, record_limit)
    times_map = {}
    positions = []
    for item in data:
        p = item["网格"]
        if p not in times_map:
            times_map[p] = [0 for _ in range(24)]
            positions.append(p)
        time_hour = int(item["上次核酸检测时间"].hour)
        times_map[p][time_hour - 1] += 1
    if len(positions) == 0:
        grids = get_grids(db, date)
        for g in grids:
            positions.append(g["网格"])
            times_map[g["网格"]] = [0 for _ in range(24)]
    positions.sort()
    return jsonify({"recordsTime": times_map, "positions": positions}, 200, {"Content-Type": "application/json"})


@app.route('/api/getHousingCnt', methods=['POST', 'GET'])
def get_housings_cnt():
    params = request.json
    date = params["date"]
    record_limit = params["recordLimit"]
    date_tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
    date_next = date_tmp + datetime.timedelta(days=1)
    date_record = date_tmp - datetime.timedelta(days=record_limit)
    grids_total_cnt = get_housings_whitelist(db, date)
    grid_finish_cnt = get_housing_finished(db, date, record_limit)

    grid_info_map = {}
    for item in grids_total_cnt:
        grid_info_map.update({
            item["小区"]: {"totalCnt": item["cnt"],
                         "finishedCnt": 0}
        })
    for item in grid_finish_cnt:
        grid_info_map[item["小区"]].update({
            "finishedCnt": item["cnt"]
        })
    return jsonify(grid_info_map, 200, {"Content-Type": "application/json"})


@app.route('/api/getHousingTimeInfo', methods=['POST', 'GET'])
def get_housing_time_info():
    params = request.json
    date = params["date"]
    limit_record = params["recordLimit"]
    date_tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
    date_next = date_tmp + datetime.timedelta(days=1)
    record_limit = date_tmp - datetime.timedelta(days=limit_record)
    data = get_housing_record_time(db, date, record_limit)
    times_map = {}
    positions = []
    for item in data:
        p = item["小区"]
        if p not in times_map:
            times_map[p] = [0 for _ in range(24)]
            positions.append(p)
        time_hour = int(item["上次核酸检测时间"].hour)
        times_map[p][time_hour - 1] += 1
    if len(positions) == 0:
        housing = get_housing(db)
        for g in housing:
            positions.append(g["小区"])
            times_map[g["小区"]] = [0 for _ in range(24)]
    positions.sort()
    return jsonify({"recordsTime": times_map, "positions": positions}, 200, {"Content-Type": "application/json"})


@app.route('/api/getExportReport', methods=['POST', 'GET'])
def get_export_report():
    params = request.json
    date = params["date"]
    parsed_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    record_limit = parsed_date - datetime.timedelta(days=1)

    grids_total_cnt = get_grid_whitelist(db, date)
    data = get_grids_record_time(db, date, record_limit)
    grids_charges = get_grids_charge(db)
    times_map, positions = {}, []
    for item in data:
        p = item["网格"]
        if p not in times_map:
            times_map[p] = [0 for _ in range(24)]
            positions.append(p)
        time_hour = int(item["上次核酸检测时间"].hour)
        times_map[p][time_hour - 1] += 1
    positions.sort()

    report = pd.DataFrame(columns=["网格", "网格员", "应采样", "完成率",
                                   "1时", "2时", "3时", "4时", "5时", "6时", "7时", "8时",
                                   "9时", "10时", "11时", "12时", "13时", "14时", "15时", "16时",
                                   "17时", "18时", "19时", "20时", "21时", "22时", "23时", "24时", ],
                          index=[])
    for index, grid in enumerate(positions):
        data = times_map[grid]

        total_cnt, finished_cnt = 0, sum(data)
        grids_charge = ""
        for item in grids_total_cnt:
            if item["网格"] == grid:
                total_cnt = item["cnt"]
                break
        for item in grids_charges:
            if item["网格号"] == grid:
                grids_charge = item["姓名"]
                break

        rate = f"{round(finished_cnt / total_cnt * 100, 2)}%"

        report.loc[index] = [grid, grids_charge, total_cnt, rate] + data
    if not os.path.exists('reports'):
        os.mkdir('reports')
    writer = pd.ExcelWriter(f'reports/{date}浪心社区网格统计情况.xlsx')
    report.to_excel(writer, startcol=0, startrow=0, index=False)
    # worksheet = writer.sheets['Sheet1']
    # worksheet.write_string(0, 0, f'{date}浪心社区网格统计情况')
    writer.save()

    community_total_cnt = get_community_whitelist(db, date)
    community_data = get_community_record_time(db, date, record_limit)
    community_time_map, people_num_map, communities = {}, {}, []
    for item in community_data:
        p = item["小区"]
        if p not in community_time_map:
            community_time_map[p] = [0 for _ in range(24)]
            communities.append(p)
        time_hour = int(item["上次核酸检测时间"].hour)
        community_time_map[p][time_hour - 1] += 1

        if p not in people_num_map:
            people_num_map[p] = 0
        people_num_map[p] += 1
    communities.sort()

    community_report = pd.DataFrame(columns=["小区", "应采样", "完成率",
                                             "1时", "2时", "3时", "4时", "5时", "6时", "7时", "8时",
                                             "9时", "10时", "11时", "12时", "13时", "14时", "15时", "16时",
                                             "17时", "18时", "19时", "20时", "21时", "22时", "23时", "24时", ],
                                    index=[])
    for index, community in enumerate(communities):
        data = community_time_map[community]

        total_cnt, finished_cnt = 0, sum(data)
        for item in community_total_cnt:
            if item["小区"] == community:
                total_cnt = item["cnt"]
                break
        rate = f"{round(finished_cnt / total_cnt * 100, 2)}%"
        community_report.loc[index] = [community, total_cnt, rate] + data

    community_writer = pd.ExcelWriter(f'reports/{date}浪心社区小区统计情况.xlsx')
    community_report.to_excel(community_writer, startcol=0, startrow=0, index=False)
    community_writer.save()
    return jsonify(1, 200, {"Content-Type": "application/json"})


def main():
    app.run(debug=True, host="0.0.0.0", port="9999")


if __name__ == '__main__':
    main()
