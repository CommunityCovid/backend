-- create a new temporary table storing new covid records
CREATE TABLE langxin_community.new_covid_detection_records (
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