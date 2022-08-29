-- move left people away from whitelist
UPDATE langxin_community.residents r join
(select distinct(r.证件号码) as 证件号码
from langxin_community.residents r left join
    langxin_community.new_residents nr
on
    r.证件号码 = nr.证件号码
where
    nr.证件号码 is null
) leave_r
on
    r.证件号码 = leave_r.证件号码
set
    r.是否在白名单 = '否';