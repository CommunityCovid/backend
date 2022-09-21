UPDATE langxin_community.residents r join
(select r.证件号码, g.灰名单类型, g.灰名单原因
from
     residents r right join
     gray_list g
on
    r.证件号码 = g.证件号码 and
    r.是否在白名单 = '是'
where r.证件号码 is not null) g
on
    r.证件号码 = g.证件号码 and
    r.是否在白名单 = '是'
set
    r.是否在灰名单 = '是',
    r.灰名单类型 = g.灰名单类型,
    r.灰名单原因 = g.灰名单原因;
