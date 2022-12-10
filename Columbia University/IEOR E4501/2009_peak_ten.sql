
with all_trips as (
    SELECT distance,
        pickup_datetime
    FROM taxi_trips
    where strftime('%Y', pickup_datetime) = '2009'
    union all
    SELECT distance,
        pickup_datetime
    FROM uber_trips
    where strftime('%Y', pickup_datetime) = '2009'
)
select strftime('%Y-%m-%d', pickup_datetime), count(1) as popularity, avg(distance) as avg_dist
from all_trips
group by strftime('%Y-%m-%d', pickup_datetime)
order by popularity desc
limit 10
