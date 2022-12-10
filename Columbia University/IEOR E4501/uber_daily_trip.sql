
select count(1) as popularity, strftime('%w', pickup_datetime) as day_of_week
from uber_trips
where strftime('%s', pickup_datetime) BETWEEN strftime('%s', '2009-01-01') AND strftime('%s', '2015-06-30')
group by strftime('%w', pickup_datetime)
order by popularity desc
