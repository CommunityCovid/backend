-- update records varied: newly released detection results
UPDATE langxin_community.covid_detection_records cdr join
(select ncdr.`证件号码` as 证件号码,ncdr.`采样时间` as 采样时间,ncdr.`检测机构` as 检测机构,ncdr.`检测时间` as 检测时间,
       ncdr.`检测结果` as 检测结果,ncdr.`检测结果填报时间` as 检测结果填报时间,ncdr.`复核结果` as 复核结果,
       ncdr.`复核机构` as 复核机构,ncdr.`复核时间` as 复核时间,ncdr.`导入时间` as 导入时间,ncdr.`创建人账号` as 创建人账号,
       ncdr.`创建人姓名` as 创建人姓名
from
    langxin_community.covid_detection_records cdr join
    langxin_community.new_covid_detection_records ncdr
on
    cdr.采样时间 = ncdr.采样时间 and
    cdr.证件号码 = ncdr.证件号码 ) updated_records
on
    cdr.采样时间 = updated_records.采样时间 and
    cdr.证件号码 = updated_records.证件号码
set
    cdr.检测机构 = updated_records.检测机构,
    cdr.检测时间 = updated_records.检测时间,
    cdr.检测结果 = updated_records.检测结果,
    cdr.检测结果填报时间 = updated_records.检测结果填报时间,
    cdr.复核结果 = updated_records.复核结果,
    cdr.复核机构 = updated_records.复核机构,
    cdr.复核时间 = updated_records.复核时间,
    cdr.导入时间 = updated_records.导入时间,
    cdr.创建人账号 = updated_records.创建人账号,
    cdr.创建人姓名 = updated_records.创建人姓名;