UPDATE langxin_community.residents_accumulative r join
    gray_list gl
on
    r.证件号码 = gl.证件号码 and
    r.加入白名单时间 <= DATE(NOW()) and
    (移出白名单时间 >= DATE(NOW()) or 移出白名单时间 is null)
set
    r.是否在灰名单 = '是',
    r.灰名单类型 = gl.灰名单类型,
    r.灰名单原因 = gl.灰名单原因;