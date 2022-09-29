-- add new records into table.
insert into langxin_community.covid_detection_records (`姓名`,`采样时间`,`证件类型`,`证件号码`)
select ncdr.`姓名`, ncdr.`采样时间`,ncdr.`证件类型`,ncdr.`证件号码`
from
    langxin_community.covid_detection_records cdr right join
    langxin_community.new_covid_detection_records ncdr
on
    cdr.证件号码 = ncdr.证件号码 and
    cdr.采样时间 = ncdr.采样时间
where
    cdr.id is NULL;