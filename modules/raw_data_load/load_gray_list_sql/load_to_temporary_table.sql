LOAD DATA INFILE 'secure_file_priv/gray_list.csv' INTO TABLE langxin_community.gray_list
CHARACTER SET utf8 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES
(`姓名`, `证件号码`,`灰名单类型`,`灰名单原因`);