-- move people not in whitelist of certain date
update langxin_community.residents r left join
    langxin_community.new_residents nr
on
    r.证件号码 = nr.证件号码 and
    r.房屋编码 = nr.房屋编码 and
    r.审核时间 = nr.审核时间
set
    r.是否在白名单 = '否',
    r.移出白名单时间 = DATE_SUB(DATE('{date}'), INTERVAL 1 SECOND)
where
    nr.证件号码 is null and
    r.加入白名单时间 <= '{date}' and
    (r.移出白名单时间 >= '{date}' or r.移出白名单时间 is null);