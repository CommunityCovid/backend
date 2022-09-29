# delete added whitelist from new_residents_accumulative
delete nra
from
    new_residents_accumulative nra left join
    residents_accumulative ra
on
    ra.加入白名单时间 = '{date}' and
    ra.证件号码 = nra.证件号码 and
    ra.房屋编码 = nra.房屋编码
where
    ra.证件号码 is not null;