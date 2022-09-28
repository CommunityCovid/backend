UPDATE langxin_community.new_residents_accumulative nra join
    gray_list gl
on
    nra.证件号码 = gl.证件号码
set
    nra.是否在灰名单 = '是',
    nra.灰名单类型 = gl.灰名单类型,
    nra.灰名单原因 = gl.灰名单原因;