select count(*) from residents_accumulative
where 加入白名单时间 = '{date}' and
      上次核酸检测时间 < DATE_ADD('{date}', INTERVAL 1 DAY) and
      上次核酸检测时间 >= DATE_SUB('{date}', INTERVAL {interval} DAY );
