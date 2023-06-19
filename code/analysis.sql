
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
