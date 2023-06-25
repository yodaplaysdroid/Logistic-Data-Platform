// 创建物流表
create table 物流公司 (
公司名称 varchar(100) not null unique,
客户编号 varchar(50) not null,
联系人 varchar(50),
电话 varchar(20),
省市区 varchar(100),
primary key(客户编号))

create table 客户信息 (
客户名称 varchar(50) not null,
客户编号 varchar(20) not null,
手机号 varchar(20) not null unique,
省市区 varchar(100),
primary key(客户编号))

create table 物流信息 (
提单号 varchar(50) not null,
货主名称 varchar(50) not null,
货主代码 varchar(20) not null foreign key references 客户信息(客户编号),
物流公司_货代 varchar(100) not null foreign key references 物流公司(公司名称),
集装箱箱号 varchar(50) not null,
货物名称 varchar(50) not null,
货重_吨 varchar(50) not null,
primary key(提单号))

create table 集装箱动态 (
堆存港口 varchar(100) not null,
集装箱箱号 varchar(50) not null,
箱尺寸_TEU varchar(50),
提单号 varchar(100) not null foreign key references 物流信息(提单号),
堆场位置 varchar(100) not null,
操作 varchar(50) not null,
操作日期 varchar(50) not null,
primary key(集装箱箱号, 提单号, 操作))

create table 装货表 (
船公司 varchar(100),
船名称 varchar(100),
作业开始时间 varchar(100),
作业结束时间 varchar(100),
始发时间 varchar(100),
到达时间 varchar(100),
作业港口 varchar(100),
提单号 varchar(100) not null foreign key references 物流信息(提单号),
集装箱箱号 varchar(100),
箱尺寸_TEU varchar(100),
启运地 varchar(100),
目的地 varchar(100),
primary key(提单号))

create table 卸货表 (
船公司 varchar(100),
船名称 varchar(100),
作业开始时间 varchar(100),
作业结束时间 varchar(100),
始发时间 varchar(100),
到达时间 varchar(100),
作业港口 varchar(100),
提单号 varchar(100) not null foreign key references 物流信息(提单号),
集装箱箱号 varchar(100),
箱尺寸_TEU varchar(100),
启运地 varchar(100),
目的地 varchar(100),
primary key(提单号))

create table 假客户信息 (
客户名称 varchar(50),
客户编号 varchar(20),
手机号 varchar(20),
省市区 varchar(100))


// 港口吞吐量分析
create view 分析一 as
select 集装箱动态.堆存港口, count(集装箱动态.提单号)/2 as 数量吞吐量, sum(物流信息.货重_吨/(LENGTH(物流信息.集装箱箱号)-LENGTH(REPLACE(物流信息.集装箱箱号, ',', ''))+1))/2 AS 货重吞吐量
from 物流信息, 集装箱动态
where 物流信息.提单号 = 集装箱动态.提单号
group by 集装箱动态.堆存港口

// 港口不同类型货物吞吐量趋势
create view 分析二 as
select 货物名称, count(货重_吨) as 客户量, sum(货重_吨) as 总货重
from 物流信息
group by 货物名称
order by 总货重 desc, 客户量 desc

// 港口货物吞吐同比环比
create view 分析三 as
select substring(集装箱动态.操作日期, 1, 7) as 年月, 物流信息.货物名称, sum(物流信息.货重_吨/(LENGTH(物流信息.集装箱箱号) - LENGTH(REPLACE(物流信息.集装箱箱号, ',', ''))+1))/2 AS 总货重
from 物流信息, 集装箱动态
where 物流信息.提单号 = 集装箱动态.提单号 
group by substring(集装箱动态.操作日期, 1, 7), 物流信息.货物名称
ORDER BY substring(集装箱动态.操作日期, 1, 7), 总货重 desc

// 不同货物吞吐量占比
create view 分析四 as
select 货物名称, (cast (count(货重_吨) as decimal)*100/(select count(货重_吨) from 物流信息)) as 客户量, (sum(货重_吨)*100/(select sum(货重_吨) from 物流信息)) as 总量
from 物流信息
group by 货物名称
order by 总量 desc, 客户量 desc

// 不同货物流向分析
create view 分析五 as
select 集装箱动态.堆存港口, 物流信息.货物名称, count(集装箱动态.提单号)/2 as 数量吞吐量, sum(物流信息.货重_吨/(LENGTH(物流信息.集装箱箱号)-LENGTH(REPLACE(物流信息.集装箱箱号, ',', ''))+1))/2 AS 总货重
from 物流信息, 集装箱动态
where 物流信息.提单号 = 集装箱动态.提单号
group by 集装箱动态.堆存港口, 物流信息.货物名称
order by 集装箱动态.堆存港口, 物流信息.货物名称

// 不同类型货物堆场流转周期分析
create view 分析六 as
select 物流信息.货物名称, avg(datediff(day, 装货表.作业开始时间, 卸货表.作业结束时间)) as 时间消耗_日, avg(datediff(hh, 装货表.作业开始时间, 卸货表.作业结束时间)) as 时间消耗_小时
from 装货表, 卸货表, 物流信息
where 装货表.提单号 = 卸货表.提单号
and 装货表.集装箱箱号 = 卸货表.集装箱箱号
and 装货表.提单号 = 物流信息.提单号
group by 物流信息.货物名称
order by 时间消耗_日

create view 分析3 as
select s1.货物名称, sum(s1.总货重) as y1, sum(s2.总货重) as y2, (sum(s2.总货重) - sum(s1.总货重)) as y3 from
(select * from 分析三 where 年月 like '%-12%') as s1,
(select * from 分析三 where 年月 like '%-11%') as s2
where s1.货物名称 = s2.货物名称
group by s1.货物名称;

create view 分析5 as
select 货物名称 as x, 数量吞吐量, 总货重 from 分析五 where 堆存港口 = '杭州港';

// 主页分析1
SELECT 货物名称, count(货重_吨)
FROM 集装箱动态, 物流信息
WHERE 物流信息.提单号 = 集装箱动态.提单号
and 操作日期 in (select distinct 操作日期 from 集装箱动态 where substring(操作日期, 1, 7) in (select distinct 年月 from 分析三 order by 年月 desc limit 3))
group by 货物名称
order by count(货重_吨) desc
limit 3;

// 主页分析2
select 货物名称, count(总货重), sum(总货重) from 分析三 where 年月 in (
select distinct 年月 from 分析三 order by 年月 desc limit 3)
group by 货物名称
order by count(总货重), sum(总货重) desc
limit 3;

// 主页分析3
select substring(省市区, 1, 2), count(提单号)
from 客户信息, 物流信息
where 货主代码=客户编号
group by substring(省市区, 1, 2)
order by count(提单号) desc
limit 3;

// 主页分析4
select 堆存港口, count(提单号)
from 集装箱动态
where 操作='入库'
group by 堆存港口
order by count(提单号) desc
limit 3;

select 堆存港口, count(提单号)
from 集装箱动态
where 操作='出库'
group by 堆存港口
order by count(提单号) desc
limit 3;

// 主页分析5
select substring(装货表.作业开始时间, 1, 7), avg(datediff(day, 装货表.作业开始时间, 卸货表.作业结束时间)) as 时间
from 装货表, 卸货表
where 装货表.提单号 = 卸货表.提单号
group by substring(装货表.作业开始时间, 1, 7)
order by substring(装货表.作业开始时间, 1, 7) desc