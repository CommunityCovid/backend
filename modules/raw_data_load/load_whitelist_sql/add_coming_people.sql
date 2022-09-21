insert into langxin_community.residents (`街道`,`社区`,`网格`,`所居住花园小区/城中村名称`,`所属电子哨兵卡口名称`,`姓名`,`性别`,`人员类型`,`证件类型`,`证件号码`,
 `出生年月`,`手机号码`,`国籍`,`是否暂离`,`户籍地址`,`工作单位所在市`,`工作单位所在行政区`,`工作单位名称`,`工作单位地址`,
 `是否纳入市网格办统计`,`楼栋地址`,`楼栋编码`,`房屋地址`,`房屋编码`,`备注`,`审核结果`,`审核人`,`审核时间`,`上报类型`,`加入白名单时间`, `移出白名单时间`)
select nr.`街道`,nr.`社区`,nr.`网格`,nr.`所居住花园小区/城中村名称`,nr.`所属电子哨兵卡口名称`,nr.`姓名`,nr.`性别`,nr.`人员类型`,
       nr.`证件类型`,nr.`证件号码`,nr.`出生年月`,nr.`手机号码`,nr.`国籍`,nr.`是否暂离`,nr.`户籍地址`,nr.`工作单位所在市`,
       nr.`工作单位所在行政区`,nr.`工作单位名称`,nr.`工作单位地址`,nr.`是否纳入市网格办统计`,nr.`楼栋地址`,nr.`楼栋编码`,nr.`房屋地址`,
       nr.`房屋编码`,nr.`备注`,nr.`审核结果`,nr.`审核人`,nr.`审核时间`,nr.`上报类型`, '{date}',
       IF((select count(*) from langxin_community.residents where 加入白名单时间 > '{date}' or 移出白名单时间 > '{date}') > 0,
          (IF((select min(移出白名单时间) from residents where 移出白名单时间 > '{date}') is not null,
           (select date_sub(date(date_add(least(min(加入白名单时间), min(移出白名单时间)), INTERVAL 1 SECOND)), INTERVAL 1 SECOND) from langxin_community.residents
          where 加入白名单时间 > '{date}' or (移出白名单时间 > '{date}' and 移出白名单时间 is not null)),
          (select date_sub(min(加入白名单时间), INTERVAL 1 SECOND) from langxin_community.residents
          where 加入白名单时间 > '{date}' or (移出白名单时间 > '{date}' and 移出白名单时间 is not null))))
          , null)
from
    langxin_community.residents r right join
    langxin_community.new_residents nr
on
    r.证件号码 = nr.证件号码 and
    r.房屋编码 = nr.房屋编码 and
    r.审核时间 = nr.审核时间
where
    r.证件号码 is null;