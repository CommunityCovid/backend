-- 1.浪心村 &
update langxin_community.residents set 小区 = '浪心村'
where `所居住花园小区/城中村名称` LIKE '%浪心一路%'
or `所居住花园小区/城中村名称` LIKE '%浪心二路%'
or `所居住花园小区/城中村名称` LIKE '%浪心南路%'
or `所居住花园小区/城中村名称` LIKE '%浪心旧村%'
or `所居住花园小区/城中村名称` LIKE '%罗租路%'
or `所居住花园小区/城中村名称` LIKE '%浪心村%'
or `所居住花园小区/城中村名称` REGEXP '.*宝石南路1(0[2468]|[1-7][02468]|80)号.*';

-- 2.砖厂村 &
update langxin_community.residents set 小区 = '砖厂村'
where `所居住花园小区/城中村名称` LIKE '%砖厂新村%'
or `所居住花园小区/城中村名称` LIKE '%砖厂老村%'
or `所居住花园小区/城中村名称` LIKE '%砖厂村%'
or `所居住花园小区/城中村名称` REGEXP '.*砖厂路([2-9][13579]|1[0-9]|[1-9])号.*';

-- 3.河滨花园 &
update langxin_community.residents set 小区 = '河滨花园'
where `所居住花园小区/城中村名称` LIKE '%河滨花园%'
or `所居住花园小区/城中村名称` LIKE '%宝石南路188号%';

-- 4.石岩市场 &
update langxin_community.residents set 小区 = '石岩市场'
where `所居住花园小区/城中村名称` LIKE '%石岩市场%';

-- 5.浪心车头村 &
update langxin_community.residents set 小区 = '浪心车头村'
where `所居住花园小区/城中村名称` LIKE '%车头村%'
or `所居住花园小区/城中村名称` LIKE '%民致富商业街23号%'
or `所居住花园小区/城中村名称` LIKE '%民致富商业街25号%'
or `所居住花园小区/城中村名称` LIKE '%民致富商业街27号%'
or `所居住花园小区/城中村名称` LIKE '%民致富商业街29号%';

-- 6.浪心新村 &
update langxin_community.residents set 小区 = '浪心新村'
where `所居住花园小区/城中村名称` LIKE '%浪心新村%';

-- 7.浪心西村 &
update langxin_community.residents set 小区 = '浪心西村'
where `所居住花园小区/城中村名称` LIKE '%浪心西村%';

-- 8.港湖新村 &
update langxin_community.residents set 小区 = '港湖新村'
where `所居住花园小区/城中村名称` LIKE '%港湖新村%';

-- 9.石岩新村 &
update langxin_community.residents set 小区 = '石岩新村'
where `所居住花园小区/城中村名称` LIKE '%石岩新村%'
or `所居住花园小区/城中村名称` LIKE '%青年西路2号%'
or `所居住花园小区/城中村名称` LIKE '%青年西路4号%'
or `所居住花园小区/城中村名称` LIKE '%青年西路6号%'
or `所居住花园小区/城中村名称` LIKE '%青年西路8号%';

-- 10.王家庄 &
update langxin_community.residents set 小区 = '王家庄'
where `所居住花园小区/城中村名称` LIKE '%王家庄%'
or `所居住花园小区/城中村名称` REGEXP '.*青年西路([12][02468]|30)号.*';

-- 11.信宜新村 &
update langxin_community.residents set 小区 = '信宜新村'
where `所居住花园小区/城中村名称` LIKE '%信宜新村%'
or `所居住花园小区/城中村名称` REGEXP '.*青年西路[1-3][13579]?号.*'
or `所居住花园小区/城中村名称` REGEXP '.*洲石路([1-2][02468]|[2468])号.*'
or `所居住花园小区/城中村名称` LIKE '%青年西路口%';

-- 12.山城后门 &
update langxin_community.residents set 小区 = '山城后门'
where `所居住花园小区/城中村名称` LIKE '%山城后门%'
or `所居住花园小区/城中村名称` REGEXP '.*洲石路(2[2468]|3[02468]|4[02])号.*';

-- 13.石头山小区 &
update langxin_community.residents set 小区 = '石头山小区'
where `所居住花园小区/城中村名称` LIKE '%石头山%'
or `所居住花园小区/城中村名称` REGEXP '.*洲石路(6[2468]|[7-9][02468]|10[02])号.*'
or `所居住花园小区/城中村名称` LIKE '%石头山工业区18号%'
or `所居住花园小区/城中村名称` LIKE '%石头山工业区19号%';

-- 14. 金三角 &
update langxin_community.residents set 小区 = '金三角'
where `所居住花园小区/城中村名称` LIKE '%塘头大道山城小区%';

-- 15.龙马小区 &
update langxin_community.residents set 小区 = '龙马小区'
where `所居住花园小区/城中村名称` LIKE '%山城小区%';

-- 16.松石苑 &
update langxin_community.residents set 小区 = '松石苑'
where `所居住花园小区/城中村名称` LIKE '%松石苑%'
or `所居住花园小区/城中村名称` LIKE '%青年西路17号%';

-- 17.怡人轩 &
update langxin_community.residents set 小区 = '怡人轩'
where `所居住花园小区/城中村名称` LIKE '%信宜新村22号%';

-- 18.浪心工业区 &
update langxin_community.residents set 小区 = '浪心工业区'
where `所居住花园小区/城中村名称` LIKE '%浪心工业区%';

-- 19.老添好厂 &
update langxin_community.residents set 小区 = '老添好厂'
where `所居住花园小区/城中村名称` LIKE '%添好%'
or `所居住花园小区/城中村名称` LIKE '%青年东路12号%'
or `所居住花园小区/城中村名称` LIKE '%青年东路13号%'
or `所居住花园小区/城中村名称` LIKE '%青年东路18号%'
or `所居住花园小区/城中村名称` LIKE '%青年东路19号%'
or `所居住花园小区/城中村名称` LIKE '%青年东路20号%'
or `所居住花园小区/城中村名称` LIKE '%青年东路21号%'
or `所居住花园小区/城中村名称` LIKE '%青年东路38号%';

-- 20.万效工业区 &
update langxin_community.residents set 小区 = '万效工业区'
where `所居住花园小区/城中村名称` LIKE '%万效工业园5号%'
or `所居住花园小区/城中村名称` LIKE '%万效工业园8号%'
or `所居住花园小区/城中村名称` LIKE '%万效工业园11号%';

-- 21.玉山工业区 &
update langxin_community.residents set 小区 = '玉山工业区'
where `所居住花园小区/城中村名称` LIKE '%玉山工业区%';

-- 22.华泽厂 &
update langxin_community.residents set 小区 = '华泽厂'
where `所居住花园小区/城中村名称` LIKE '%洲石路108号%';

-- 23.早进工业区 &
update langxin_community.residents set 小区 = '早进工业区'
where `所居住花园小区/城中村名称` LIKE '%早进工业区%';

-- 24.山城工业区 &
update langxin_community.residents set 小区 = '山城工业区'
where `所居住花园小区/城中村名称` LIKE '%国泰路10号%'
or `所居住花园小区/城中村名称` LIKE '%山城工业%';

-- 25.龙马工业区 &
update langxin_community.residents set 小区 = '龙马工业区'
where `所居住花园小区/城中村名称` LIKE '%龙马工业区%'
or `所居住花园小区/城中村名称` LIKE '%龙马科技%';

-- 26.万大工业区 &
update langxin_community.residents set 小区 = '万大工业区'
where `所居住花园小区/城中村名称` LIKE '%万大%';

-- 27.恒超工业区 &
update langxin_community.residents set 小区 = '恒超工业区'
where `所居住花园小区/城中村名称` LIKE '%恒超%';

-- 28.明金海工业区 &
update langxin_community.residents set 小区 = '明金海工业区'
where `所居住花园小区/城中村名称` LIKE '%明金海%';

-- 29.旭兴达工业区 &
update langxin_community.residents set 小区 = '旭兴达工业区'
where `所居住花园小区/城中村名称` LIKE '%旭兴达%';

-- 30.嘉达工业区 &
update langxin_community.residents set 小区 = '嘉达工业区'
where `所居住花园小区/城中村名称` LIKE '%嘉达%';

-- 31.宏源发花卉市场 &
update langxin_community.residents set 小区 = '宏源发花卉市场'
where `所居住花园小区/城中村名称` LIKE '%花卉%';

-- 32.宏发大世界 &
update langxin_community.residents set 小区 = '宏发大世界'
where `所居住花园小区/城中村名称` LIKE '%宝石南路95号%'
or `所居住花园小区/城中村名称` LIKE '%宏发大世界%';

-- 33.宏源发物流园 &
update langxin_community.residents set 小区 = '宏源发物流园'
where `所居住花园小区/城中村名称` LIKE '%洲石路1号%';

-- 34.中集创谷 &
update langxin_community.residents set 小区 = '中集创谷'
where `所居住花园小区/城中村名称` LIKE '%驰通%';

-- 35.飞黄达工业区 &
update langxin_community.residents set 小区 = '飞黄达工业区'
where `所居住花园小区/城中村名称` LIKE '%石头山工业区别墅%'
or `所居住花园小区/城中村名称` LIKE '%黄池林%';

-- 36.铭原鞋厂 &
update langxin_community.residents set 小区 = '铭原鞋厂'
where `所居住花园小区/城中村名称` LIKE '%铭原%';

-- 37.瀚坤食品 &
update langxin_community.residents set 小区 = '瀚坤食品'
where `所居住花园小区/城中村名称` LIKE '%瀚坤食品%';

-- 38.骏兴隆工业区 &
update langxin_community.residents set 小区 = '骏兴隆工业区'
where `所居住花园小区/城中村名称` LIKE '%骏兴隆%';

-- 39.玮力裕 &
update langxin_community.residents set 小区 = '玮力裕'
where `所居住花园小区/城中村名称` LIKE '%玮力裕%';

-- 40.石岩湖学校 &
update langxin_community.residents set 小区 = '石岩湖学校'
where `所居住花园小区/城中村名称` LIKE '%石岩湖学校%'
or `所居住花园小区/城中村名称` LIKE '%青年西路34号%';
