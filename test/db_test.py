import datetime

import matplotlib.pyplot as plt

from utils.dao2 import *


def data_base():
    db_server = DBServer()
    sql = "select cdr.采样地点,cdr.采样时间 from residents r " \
          "join covid_detection_records cdr " \
          "on r.证件号码 = cdr.证件号码 " \
          "and  cdr.采样时间 > '2022-08-25' " \
          "and cdr.采样时间 < '2022-08-26'" \
          "and locate('浪心', cdr.采样地点) > 0 ;"
    data = db_server.get_community_people(sql)
    timesMap = {}
    for item in data.values[:]:
        if item[0] not in timesMap:
            timesMap[item[0]] = []
        timesMap[item[0]].append(int(item[1].timestamp()))

    idx = 1
    for key in timesMap:
        plt.scatter(timesMap[key], [idx for _ in range(len(timesMap[key]))], alpha=0.2)
        idx += 1
    plt.show()


if __name__ == '__main__':
    data_base()
