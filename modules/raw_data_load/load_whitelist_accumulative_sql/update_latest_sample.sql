# compute 上次核酸检测时间
update new_residents_accumulative nra join
    (select cdr.证件号码 as 证件号码, MAX(cdr.采样时间) as 采样时间
    from
        covid_detection_records cdr join
        new_residents_accumulative nra
    on
        nra.证件号码 = cdr.证件号码
    where
        采样时间 <= DATE_ADD('{date}', INTERVAL 1 DAY)
    group by
        nra.证件号码) cdr
on
    nra.证件号码 = cdr.证件号码
set
    nra.上次核酸检测时间 = cdr.采样时间;