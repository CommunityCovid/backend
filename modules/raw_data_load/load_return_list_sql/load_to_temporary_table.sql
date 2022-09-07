-- load return list in csv files into temporary table
LOAD DATA INFILE 'secure_file_priv/return_list.csv' INTO TABLE langxin_community.return_list
CHARACTER SET utf8 FIELDS TERMINATED BY ',' ESCAPED BY '\\' LINES TERMINATED BY '\n'  IGNORE 1 LINES
(`社区`, `人员类型`, `分类`, `网格`, `姓名`, `证件号码`, `手机号码`, `房屋地址`, `最近采样时间`, `楼栋编码`);