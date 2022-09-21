-- move left people away from whitelist
UPDATE langxin_community.residents r join
(select distinct r.证件号码 as 证件号码, r.房屋编码 as 房屋编码
from langxin_community.residents r left join
    langxin_community.new_residents nr
on
    r.证件号码 = nr.证件号码 and
    r.房屋编码 = nr.房屋编码    
where
	r.是否在白名单 = '是' and
    nr.证件号码 is null and
	nr.是否暂离 = '正常'
) leave_r
on
    r.证件号码 = leave_r.证件号码 and
    r.房屋编码 = leave_r.房屋编码 and
    r.是否在白名单 = '是'
set
    r.是否在白名单 = '否',
    r.移出白名单时间 = DATE_SUB(DATE('{date}'), INTERVAL 1 SECOND)
