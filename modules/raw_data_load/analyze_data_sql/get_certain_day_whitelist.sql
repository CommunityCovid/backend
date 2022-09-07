-- replace 'certain_date' with the date of needed whitelist
select count(*)
from residents
where
    加入白名单时间 <= '{date}' and
    (移出白名单时间 >= '{date}' or 移出白名单时间 is null)