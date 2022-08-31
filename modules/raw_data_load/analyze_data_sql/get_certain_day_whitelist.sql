-- replace 'certain_date' with the date of needed whitelist
select *
from
     residents r
where
    DATE(DATE_ADD(r.审核时间, INTERVAL 1 DAY)) <= 'certain_date' and
    (DATE(r.移出白名单时间) > 'certain_date' or r.移出白名单时间 is null)