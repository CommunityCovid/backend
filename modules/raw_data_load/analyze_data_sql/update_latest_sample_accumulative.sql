update residents_accumulative ra join
    (select ra.加入白名单时间 as 加入白名单时间, ra.证件号码 as 证件号码, MAX(cdr.采样时间) as 采样时间
    from
        langxin_community.residents_accumulative ra join
        langxin_community.covid_detection_records cdr
    on
        ra.证件号码 = cdr.证件号码
    where
        ra.加入白名单时间 >= DATE(cdr.采样时间)
    group by ra.证件号码, ra.加入白名单时间) cdr
on
    ra.证件号码 = cdr.证件号码 and
    ra.加入白名单时间 = cdr.加入白名单时间
set
    ra.上次核酸检测时间 = cdr.采样时间;
