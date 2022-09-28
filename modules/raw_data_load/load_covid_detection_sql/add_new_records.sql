-- add new records into table.
insert into langxin_community.covid_detection_records (`姓名`,`出生日期`,`年龄`,`电话号码`,`机构所在地`,`采样机构`,`采样时间`,`检测机构`,`检测时间`,
                                     `检测结果`,`检测结果填报时间`,`复核结果`,`复核机构`,`复核时间`,`性别`,`国家/地区`,`居住地`,
                                     `证件类型`,`证件号码`,`未提供有效证件原因`,`检测人群分类`,`应检尽检类别`,`导入机构`,`样本条形码`,
                                     `样本类型`,`检测项目`,`采样点行政区划`,`采样地点`,`所在学校/单位名称`,`备注1`,`备注2`,`采集类型`,
                                     `导入时间`,`创建人账号`,`创建人姓名`)
select ncdr.`姓名`,ncdr.`出生日期`,ncdr.`年龄`,ncdr.`电话号码`,ncdr.`机构所在地`,ncdr.`采样机构`,ncdr.`采样时间`,ncdr.`检测机构`,
       ncdr.`检测时间`,ncdr.`检测结果`,ncdr.`检测结果填报时间`,ncdr.`复核结果`,ncdr.`复核机构`,ncdr.`复核时间`,ncdr.`性别`,
       ncdr.`国家/地区`,ncdr.`居住地`,ncdr.`证件类型`,ncdr.`证件号码`,ncdr.`未提供有效证件原因`,ncdr.`检测人群分类`,ncdr.`应检尽检类别`,
       ncdr.`导入机构`,ncdr.`样本条形码`,ncdr.`样本类型`,ncdr.`检测项目`,ncdr.`采样点行政区划`,ncdr.`采样地点`,ncdr.`所在学校/单位名称`,
       ncdr.`备注1`,ncdr.`备注2`,ncdr.`采集类型`,ncdr.`导入时间`,ncdr.`创建人账号`,ncdr.`创建人姓名`
from
    langxin_community.covid_detection_records cdr right join
    langxin_community.new_covid_detection_records ncdr
on
    cdr.证件号码 = ncdr.证件号码 and
    cdr.采样时间 = ncdr.采样时间
where
    cdr.id is NULL and
    ncdr.id in (select min(id) from langxin_community.new_covid_detection_records group by 证件号码, 采样时间);