LOAD DATA INFILE '/var/lib/mysql-files/whitelist.csv' INTO TABLE langxin_community.residents
CHARACTER SET utf8 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES
(`街道`,`社区`,`网格`,`所居住花园小区/城中村名称`,`所属电子哨兵卡口名称`,`姓名`,`性别`,`人员类型`,`证件类型`,`证件号码`,
 `出生年月`,`手机号码`,`国籍`,`是否暂离`,`户籍地址`,`工作单位所在市`,`工作单位所在行政区`,`工作单位名称`,`工作单位地址`,
 `是否纳入市网格办统计`,`楼栋地址`,`楼栋编码`,`房屋地址`,`房屋编码`,`备注`,`审核结果`,`审核人`,`审核时间`,`上报类型`);