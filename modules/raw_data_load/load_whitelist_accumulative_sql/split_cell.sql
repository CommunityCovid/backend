# 划分小区
update new_residents_accumulative nra join
    cell_rules cr
on
    locate(nra.楼栋地址, cr.楼栋地址) is not null and
    locate(nra.楼栋地址, cr.楼栋地址) > 0
set
    nra.小区 = cr.所属小区;