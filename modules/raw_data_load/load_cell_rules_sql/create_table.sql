-- create a new temporary table storing new covid records
CREATE TABLE langxin_community.cell_rules (
    `楼栋地址` VARCHAR(40),
    `所属小区` VARCHAR(40),
    INDEX idx_cell(`楼栋地址`)
) DEFAULT CHARSET=utf8;