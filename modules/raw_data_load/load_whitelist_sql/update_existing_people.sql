# 更新之后白名单与当前白名单匹配的用户的加入白名单时间
update langxin_community.new_residents nr left join
    langxin_community.residents r
on
    r.证件号码 = nr.证件号码 and
    r.房屋编码 = nr.房屋编码 and
    r.审核时间 = nr.审核时间
set
    r.加入白名单时间 = '{date}'
where
    r.证件号码 is not null and
    r.加入白名单时间 > DATE('{date}');