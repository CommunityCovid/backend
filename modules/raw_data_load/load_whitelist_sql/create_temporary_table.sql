CREATE TABLE langxin_community.new_residents (
    `id` INT UNSIGNED AUTO_INCREMENT,
    `街道` VARCHAR(20),
    `社区` VARCHAR(20),
    `网格` VARCHAR(20),
    `所居住花园小区/城中村名称` VARCHAR(40),
    `所属电子哨兵卡口名称` VARCHAR(100),
    `姓名` VARCHAR(100),
    `性别` VARCHAR(3),
    `人员类型` VARCHAR(20),
    `证件类型` VARCHAR(20),
    `证件号码` VARCHAR(100),
    `出生年月` DATETIME,
    `手机号码` VARCHAR(20),
    `国籍` VARCHAR(20),
    `是否暂离` VARCHAR(20),
    `户籍地址` VARCHAR(100),
    `工作单位所在市` VARCHAR(20),
    `工作单位所在行政区` VARCHAR(20),
    `工作单位名称` VARCHAR(40),
    `工作单位地址` VARCHAR(100),
    `是否纳入市网格办统计` VARCHAR(20),
    `楼栋地址` VARCHAR(100),
    `楼栋编码` VARCHAR(25),
    `房屋地址` VARCHAR(100),
    `房屋编码` VARCHAR(25),
    `备注` VARCHAR(100),
    `审核结果` VARCHAR(20),
    `审核人` VARCHAR(20),
    `审核时间` DATETIME,
    `上报类型` VARCHAR(20),
    `是否在白名单` VARCHAR(2) DEFAULT '是',
    `是否在黑名单` VARCHAR(2) DEFAULT '否',
    `上次核酸检测时间` DATETIME DEFAULT NULL,
    PRIMARY KEY (`id`),
    INDEX idx_rid(`证件号码`)
) DEFAULT CHARSET=utf8;