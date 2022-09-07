-- Insert returned covid detection records into covid_detection_records
INSERT INTO langxin_community.covid_detection_records (证件号码, 采样时间, 备注1)
select r.证件号码, DATE_ADD('{date}', INTERVAL 12 HOUR), '回流数据'
from
    langxin_community.return_list rl right join
    (select distinct(证件号码) 证件号码 from langxin_community.residents
    where 加入白名单时间 <= '{date}' and
          (移出白名单时间 >= '{date}' or 移出白名单时间 is null) and
          上次核酸检测时间 <= '{date}') r
on
    r.证件号码 = rl.证件号码
where
    rl.证件号码 is null;