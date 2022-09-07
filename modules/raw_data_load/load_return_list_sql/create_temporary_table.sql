-- create a new temporary table storing new covid records
CREATE TABLE langxin_community.return_list (
    社区 VARCHAR(20),
    人员类型 VARCHAR(40),
    分类 VARCHAR(20),
    网格 VARCHAR(20),
    姓名 VARCHAR(50),
    证件号码 VARCHAR(25),
    手机号码 VARCHAR(20),
    房屋地址 VARCHAR(100),
    最近采样时间 DATETIME,
    楼栋编码 VARCHAR(40),
    INDEX idx_id(证件号码),
    INDEX idx_sample_time(最近采样时间)
) DEFAULT CHARSET=utf8;