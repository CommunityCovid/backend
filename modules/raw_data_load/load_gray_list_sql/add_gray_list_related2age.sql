UPDATE langxin_community.residents r join
(select * from
(select 证件号码,
CASE
    WHEN d.天数 < 365*3 THEN 1
    WHEN d.天数 >= 365*80 THEN 1
    ELSE 0
END as 灰名单类型,
CASE
    WHEN d.天数 < 365*3 THEN '2岁及以下婴幼儿'
    WHEN d.天数 >= 365*80 THEN '80岁及以上老人'
END as 灰名单原因
from
(select 证件号码,DATEDIFF(DATE(NOW()),STR_TO_DATE(SUBSTR(`证件号码`, 7,8), "%Y%m%d")) as 天数
from
     langxin_community.residents
where
      证件类型 = '大陆居民身份证' and
      是否在白名单 = '是') d) g
where
      灰名单类型 = 1) g
on
    g.证件号码 = r.证件号码 and
    r.是否在白名单 = '是' and
    r.证件类型 = '大陆居民身份证'
set
    r.是否在灰名单 = '是',
    r.灰名单类型 = g.灰名单类型,
    r.灰名单原因 = g.灰名单原因;