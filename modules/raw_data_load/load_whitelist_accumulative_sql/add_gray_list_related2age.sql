-- set gray list related to age
UPDATE langxin_community.new_residents_accumulative nra join
    (select 证件号码,
    CASE WHEN d.天数 < 365*3 THEN 1 WHEN d.天数 >= 365*80 THEN 1 ELSE 0 END as 灰名单类型,
    CASE WHEN d.天数 < 365*3 THEN '2岁及以下婴幼儿' WHEN d.天数 >= 365*80 THEN '80岁及以上老人' END as 灰名单原因
    from
        (select 证件号码,DATEDIFF('{date}',STR_TO_DATE(SUBSTR(`证件号码`, 7,8), "%Y%m%d")) as 天数
        from langxin_community.new_residents_accumulative) d)g
on
    nra.证件号码 = g.证件号码 and
    nra.证件类型 = '大陆居民身份证' and
    g.灰名单类型 = 1
set
    nra.是否在灰名单 = '是', nra.灰名单类型 = g.灰名单类型, nra.灰名单原因 = g.灰名单原因;