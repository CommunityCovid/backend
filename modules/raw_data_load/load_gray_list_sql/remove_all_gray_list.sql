-- remove all gray list records
update langxin_community.residents_accumulative
set
    是否在灰名单 = '否',
    灰名单类型 = null,
    灰名单原因 = null;