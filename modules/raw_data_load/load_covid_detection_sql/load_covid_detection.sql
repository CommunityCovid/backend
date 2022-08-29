# 1. drop temporary table storing new covid records
DROP TABLE langxin_community.new_covid_detection_records;

# 2. create a new temporary table storing new covid records
CREATE TABLE new_covid_detection_records (
    `id` INT UNSIGNED AUTO_INCREMENT,
    `姓名` VARCHAR(100),
    `出生日期` DATE,
    `年龄` INT,
    `电话号码` VARCHAR(20),
    `机构所在地` VARCHAR(100),
    `采样机构` VARCHAR(40),
    `采样时间` DATETIME,
    `检测机构` VARCHAR(40),
    `检测时间` DATETIME,
    `检测结果` VARCHAR(20),
    `检测结果填报时间` DATETIME,
    `复核结果` VARCHAR(20),
    `复核机构` VARCHAR(40),
    `复核时间` DATETIME DEFAULT NULL,
    `性别` VARCHAR(20),
    `国家/地区` VARCHAR(20),
    `居住地` VARCHAR(100),
    `证件类型` VARCHAR(20),
    `证件号码` VARCHAR(40),
    `未提供有效证件原因` VARCHAR(100),
    `检测人群分类` VARCHAR(40),
    `应检尽检类别` VARCHAR(40),
    `导入机构` VARCHAR(40),
    `样本条形码` VARCHAR(25),
    `样本类型` VARCHAR(20),
    `检测项目` VARCHAR(20),
    `采样点行政区划` VARCHAR(100),
    `采样地点` VARCHAR(100),
    `所在学校/单位名称` VARCHAR(40),
    `备注1` VARCHAR(100),
    `备注2` VARCHAR(100),
    `采集类型` VARCHAR(20),
    `导入时间` DATETIME,
    `创建人账号` VARCHAR(20),
    `创建人姓名` VARCHAR(40),
    PRIMARY KEY (`id`),
    INDEX idx_rid(`证件号码`),
    INDEX idx_sample_time(`采样时间`),
    INDEX idx_detection_result_time(`检测结果填报时间`)
) DEFAULT CHARSET=utf8;

# 3. load new detection records in csv files into temporary table
LOAD DATA INFILE '/var/lib/mysql-files/covid_detection.csv' INTO TABLE langxin_community.new_covid_detection_records
CHARACTER SET utf8 FIELDS TERMINATED BY ',' ESCAPED BY '\\' LINES TERMINATED BY '\n'  IGNORE 1 LINES
(`姓名`,`出生日期`,`年龄`,`电话号码`,`机构所在地`,`采样机构`,`采样时间`,`检测机构`,`检测时间`,`检测结果`,`检测结果填报时间`,
 `复核结果`,`复核机构`,`复核时间`,`性别`,`国家/地区`,`居住地`,`证件类型`,`证件号码`,`未提供有效证件原因`,`检测人群分类`,`应检尽检类别`,
 `导入机构`,`样本条形码`,`样本类型`,`检测项目`,`采样点行政区划`,`采样地点`,`所在学校/单位名称`,`备注1`,`备注2`,`采集类型`,`导入时间`,
 `创建人账号`,`创建人姓名`);

# 4. merge temporary table into main table of covid detection records
# 4.1 update records varied: newly released detection results
UPDATE covid_detection_records cdr join
(select ncdr.`证件号码` as 证件号码,ncdr.`采样时间` as 采样时间,ncdr.`检测机构` as 检测机构,ncdr.`检测时间` as 检测时间,
       ncdr.`检测结果` as 检测结果,ncdr.`检测结果填报时间` as 检测结果填报时间,ncdr.`复核结果` as 复核结果,
       ncdr.`复核机构` as 复核机构,ncdr.`复核时间` as 复核时间,ncdr.`导入时间` as 导入时间,ncdr.`创建人账号` as 创建人账号,
       ncdr.`创建人姓名` as 创建人姓名
from
    covid_detection_records cdr join
    new_covid_detection_records ncdr
on
    cdr.采样时间 = ncdr.采样时间 and
    cdr.证件号码 = ncdr.证件号码 ) updated_records
on
    cdr.采样时间 = updated_records.采样时间 and
    cdr.证件号码 = updated_records.证件号码
set
    cdr.检测机构 = updated_records.检测机构,
    cdr.检测时间 = updated_records.检测时间,
    cdr.检测结果 = updated_records.检测结果,
    cdr.检测结果填报时间 = updated_records.检测结果填报时间,
    cdr.复核结果 = updated_records.复核结果,
    cdr.复核机构 = updated_records.复核机构,
    cdr.复核时间 = updated_records.复核时间,
    cdr.导入时间 = updated_records.导入时间,
    cdr.创建人账号 = updated_records.创建人账号,
    cdr.创建人姓名 = updated_records.创建人姓名;

# 4.2.add new records into table.
insert into covid_detection_records (`姓名`,`出生日期`,`年龄`,`电话号码`,`机构所在地`,`采样机构`,`采样时间`,`检测机构`,`检测时间`,
                                     `检测结果`,`检测结果填报时间`,`复核结果`,`复核机构`,`复核时间`,`性别`,`国家/地区`,`居住地`,
                                     `证件类型`,`证件号码`,`未提供有效证件原因`,`检测人群分类`,`应检尽检类别`,`导入机构`,`样本条形码`,
                                     `样本类型`,`检测项目`,`采样点行政区划`,`采样地点`,`所在学校/单位名称`,`备注1`,`备注2`,`采集类型`,
                                     `导入时间`,`创建人账号`,`创建人姓名`)
select ncdr.`姓名`,ncdr.`出生日期`,ncdr.`年龄`,ncdr.`电话号码`,ncdr.`机构所在地`,ncdr.`采样机构`,ncdr.`采样时间`,ncdr.`检测机构`,
       ncdr.`检测时间`,ncdr.`检测结果`,ncdr.`检测结果填报时间`,ncdr.`复核结果`,ncdr.`复核机构`,ncdr.`复核时间`,ncdr.`性别`,
       ncdr.`国家/地区`,ncdr.`居住地`,ncdr.`证件类型`,ncdr.`证件号码`,ncdr.`未提供有效证件原因`,ncdr.`检测人群分类`,ncdr.`应检尽检类别`,
       ncdr.`导入机构`,ncdr.`样本条形码`,ncdr.`样本类型`,ncdr.`检测项目`,ncdr.`采样点行政区划`,ncdr.`采样地点`,ncdr.`所在学校/单位名称`,
       ncdr.`备注1`,ncdr.`备注2`,ncdr.`采集类型`,ncdr.`导入时间`,ncdr.`创建人账号`,ncdr.`创建人姓名`
from
    covid_detection_records cdr right join
    new_covid_detection_records ncdr
on
    cdr.证件号码 = ncdr.证件号码
    and cdr.采样时间 = ncdr.采样时间
where
    cdr.id is NULL;

