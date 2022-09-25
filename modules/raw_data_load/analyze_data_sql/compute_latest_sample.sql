UPDATE
    residents join
    (select MAX(采样时间) as 采样时间, 证件号码 from covid_detection_records group by 证件号码) latest_sample_time
on
    residents.证件号码 = latest_sample_time.证件号码
set
    residents.上次核酸检测时间 = latest_sample_time.采样时间;