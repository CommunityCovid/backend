CREATE TABLE IF NOT EXISTS gray_list (
    `姓名` VARCHAR(20),
    `证件号码` VARCHAR(25),
    `灰名单类型` INT,
    `灰名单原因` VARCHAR(100),
    INDEX idx_id(`证件号码`)
) DEFAULT CHARSET=utf8;