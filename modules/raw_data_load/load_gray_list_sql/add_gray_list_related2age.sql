UPDATE langxin_community.residents_accumulative r join
    (select 证件号码,
    CASE WHEN d.天数 < 365*3 THEN 1 WHEN d.天数 >= 365*80 THEN 1 ELSE 0 END as 灰名单类型,
    CASE WHEN d.天数 < 365*3 THEN '2岁及以下婴幼儿' WHEN d.天数 >= 365*80 THEN '80岁及以上老人' END as 灰名单原因
    from
        (select 证件号码,DATEDIFF(DATE(NOW()),STR_TO_DATE(SUBSTR(`证件号码`, 7,8), "%Y%m%d")) as 天数
        from langxin_community.residents_accumulative) d)g
on
    r.证件号码 = g.证件号码 and
    加入白名单时间 <= DATE(NOW()) and
    (移出白名单时间 >= DATE(NOW()) or 移出白名单时间 is null) and
    r.证件类型 = '大陆居民身份证' and
    g.灰名单类型 = 1
set
    r.是否在灰名单 = '是', r.灰名单类型 = g.灰名单类型, r.灰名单原因 = g.灰名单原因;