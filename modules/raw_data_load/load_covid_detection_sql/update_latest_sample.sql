# use new covid detection records to update whitelist
update residents_accumulative ra join
    new_covid_detection_records ncdr
on
    ra.证件号码 = ncdr.证件号码
set ra.上次核酸检测时间 = ncdr.采样时间
where ra.加入白名单时间 >= '{date}' and
    (ra.上次核酸检测时间 < '{date}' or ra.上次核酸检测时间 is null)