import datetime
import logging
import re
import string

import matplotlib.pyplot as plt
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask import render_template, Response, json, make_response
import os

from utils.util import *
from utils.dao import *
from utils.dao2 import *

from utils.statics import *
from flask_mysqldb import MySQL

FILE_ABS_PATH = os.path.dirname(__file__)
DATA_DIR = os.path.join(FILE_ABS_PATH, 'data')

app = Flask(__name__)
CORS(app)

db_server = None

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_HOST'] = '10.20.4.104'
app.config['MYSQL_DB'] = 'langxin_community'
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
    # date = params['date']

    total_cnt = get_whitelist_num(db)
    finished_cnt = get_finished_num(db)
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
    print(date_tmp, date_next)
    grids_total_cnt = get_grid_whitelist(db, date_tmp)
    grid_finish_cnt = get_grid_finished(db, date_tmp, date_next)

    grid_info_map = {}
    for item in grids_total_cnt:
        grid_info_map.update({
            item["网格"]: {"totalCnt": item["cnt"]}
        })
    for item in grid_finish_cnt:
        grid_info_map[item["网格"]].update({
            "finishedCnt": item["cnt"]
        })
    return jsonify(grid_info_map, 200, {"Content-Type": "application/json"})


@app.route('/api/getCommunityPeople', methods=['POST', 'GET'])
def get_whitelist():
    whitelist = get_whitelist()
    values = []
    for item in whitelist:
        values.append([item[key] for key in residents_columns])
    return jsonify({"columns": residents_columns, "people": values}, 200, {"Content-Type": "application/json"})


@app.route('/api/getGridPeople', methods=['POST', 'GET'])
def get_grid_people():
    params = request.json
    grid = params["grid"]
    whitelist = get_grid_whitelist_people(db, grid)
    values = []
    for item in whitelist:
        values.append([item[key] for key in residents_columns])
    return jsonify({"columns": residents_columns, "people": values}, 200, {"Content-Type": "application/json"})


@app.route('/api/uploadFile', methods=['POST', 'GET'])
def upload_file():
    file = request.files.get("file")
    file_name = request.form.get("name")
    file.save(f"data/{file_name}")
    # logging.info(f"receive and store file {file_name} in './data'")
    print(f"receive and store file {file_name} in './data'")
    return jsonify({}, 200, {"Content-Type": "application/json"})


@app.route('/api/getRecords', methods=['POST', 'GET'])
def get_records():
    params = request.json
    date = params["date"]
    limit_record = params["recordLimit"]

    print(date)
    date_tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
    date_next = date_tmp + datetime.timedelta(days=1)
    print(date_tmp, date_next)
    data = get_records_position(db, date_tmp, date_next)
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
            res[p][t - 1] += 1
    return jsonify({"heatMap": res, "position": position}, 200, {"Content-Type": "application/json"})


@app.route('/api/getGridsTimeInfo', methods=['POST', 'GET'])
def get_grids_time_info():
    params = request.json
    date = params["date"]
    limit_record = params["recordLimit"]
    date_tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
    date_next = date_tmp + datetime.timedelta(days=1)
    record_limit = date_tmp - datetime.timedelta(days=limit_record)
    data = get_grids_record_time(db, record_limit)
    times_map = {}
    positions = []
    for item in data:
        p = item["网格"]
        if p not in times_map:
            times_map[p] = [0 for _ in range(24)]
            positions.append(p)
        time_hour = int(item["上次核酸检测时间"].hour)
        times_map[p][time_hour - 1] += 1
    positions.sort()
    return jsonify({"recordsTime": times_map, "positions": positions}, 200, {"Content-Type": "application/json"})


def main():
    app.run(debug=True, host="0.0.0.0")


if __name__ == '__main__':
    main()
