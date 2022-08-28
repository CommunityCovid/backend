import matplotlib.pyplot as plt
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask import render_template, Response, json, make_response
import os

from utils.util import *
from utils.dao import *
from utils.statics import *

FILE_ABS_PATH = os.path.dirname(__file__)
DATA_DIR = os.path.join(FILE_ABS_PATH, 'data')

app = Flask(__name__)
CORS(app)

db_server = None


def tmp_test(db_server):
    num = db_server.get_whitelist_num()
    print(num)


@app.route('/api/getCommunityCnt', methods=['POST', 'GET'])
def get_community_cnt():
    params = request.json
    # date = params['date']
    total_cnt = db_server.get_whitelist_num()
    finished_cnt = db_server.get_finished_num()
    return jsonify(
        {"totalCount": int(total_cnt),
         "finishedCnt": int(finished_cnt)
         }), 200, {"Content-Type": "application/json"}


@app.route('/api/getGridsCnt', methods=['POST', 'GET'])
def get_grids_cnt():
    params = request.json
    # date = params["date"]
    date = ""
    grids_total_cnt = db_server.get_grid_whitelist(date)
    grid_finish_cnt = db_server.get_grid_finished(date)

    grid_info_map = {}
    for item in grids_total_cnt.values:
        grid_info_map.update({
            item[0]: {"totalCnt": item[1]}
        })
    for item in grid_finish_cnt.values:
        grid_info_map[item[0]].update({
            "finishedCnt": item[1]
        })
    return jsonify(grid_info_map, 200, {"Content-Type": "application/json"})


@app.route('/api/getCommunityPeople', methods=['POST', 'GET'])
def get_whitelist():
    whitelist = db_server.get_whitelist()
    df_values = whitelist.values
    values = []
    for item in df_values:
        values.append([i for i in item])
    return jsonify({"columns": residents_columns, "people": values}, 200, {"Content-Type": "application/json"})


@app.route('/api/getGridPeople', methods=['POST', 'GET'])
def get_grid_whitelist():
    params = request.json
    grid = params["grid"]

    whitelist = db_server.get_grid_whitelist_people(grid)
    df_values = whitelist.values
    values = []
    for item in df_values:
        values.append([i for i in item])
    print(df_values)
    return jsonify({"columns": residents_columns, "people": values}, 200, {"Content-Type": "application/json"})


def main():
    global db_server
    db_server = DBServer()

    # tmp_test(db_server)

    app.run(debug=False, host="0.0.0.0")
    db_server.close()


if __name__ == '__main__':
    main()
