-- move people not in whitelist of certain date
update langxin_community.residents r left join
    (select cr.证件号码, cr.房屋编码, cr.审核时间
    from
         langxin_community.new_residents nr right join
        (select r.证件号码, r.房屋编码, r.审核时间 from langxin_community.residents r
        where r.加入白名单时间 <= '{date}' and
            (r.移出白名单时间 >= '{date}' or r.移出白名单时间 is null)) cr
    on
        nr.证件号码 = cr.证件号码 and
        nr.房屋编码 = cr.房屋编码 and
        nr.审核时间 = cr.审核时间
    where
        nr.证件号码 is null) lr
on
    r.证件号码 = lr.证件号码 and
    r.房屋编码 = lr.房屋编码 and
    r.审核时间 = lr.审核时间
set
    r.是否在白名单 = '否',
    r.移出白名单时间 = '{date}';