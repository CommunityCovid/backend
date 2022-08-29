-- load new detection records in csv files into temporary table
LOAD DATA INFILE '/var/lib/mysql-files/covid_detection.csv' INTO TABLE langxin_community.new_covid_detection_records
CHARACTER SET utf8 FIELDS TERMINATED BY ',' ESCAPED BY '\\' LINES TERMINATED BY '\n'  IGNORE 1 LINES
(`姓名`,`出生日期`,`年龄`,`电话号码`,`机构所在地`,`采样机构`,`采样时间`,`检测机构`,`检测时间`,`检测结果`,`检测结果填报时间`,
 `复核结果`,`复核机构`,`复核时间`,`性别`,`国家/地区`,`居住地`,`证件类型`,`证件号码`,`未提供有效证件原因`,`检测人群分类`,`应检尽检类别`,
 `导入机构`,`样本条形码`,`样本类型`,`检测项目`,`采样点行政区划`,`采样地点`,`所在学校/单位名称`,`备注1`,`备注2`,`采集类型`,`导入时间`,
 `创建人账号`,`创建人姓名`);