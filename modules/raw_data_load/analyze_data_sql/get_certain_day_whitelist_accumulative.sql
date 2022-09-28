-- replace 'certain_date' with the date of needed whitelist
select count(*) from langxin_community.residents_accumulative where 加入白名单时间 = '{date}';