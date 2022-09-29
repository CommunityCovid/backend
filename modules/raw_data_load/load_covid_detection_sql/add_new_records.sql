-- add new records into table.
insert into langxin_community.covid_detection_records (`姓名`,`采样时间`,`采样地点`, `证件类型`,`证件号码`)
select ncdr.`姓名`, ncdr.`采样时间`, ncdr.`采样地点`, ncdr.`证件类型`,ncdr.`证件号码`
from langxin_community.new_covid_detection_records ncdr;