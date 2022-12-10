
select strftime('%H', pickup_datetime) as hour_of_day, count(1) as popularity
from taxi_trips
where strftime('%s', pickup_datetime) BETWEEN strftime('%s', '2009-01-01') AND strftime('%s', '2015-06-30')
group by strftime('%H', pickup_datetime)
order by popularity desc
