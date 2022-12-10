
with all_trip as (
    select pickup_datetime from taxi_trips
    where strftime('%s', pickup_datetime) BETWEEN strftime('%s', '2012-10-22') AND strftime('%s', '2012-11-06')
    union all
    select pickup_datetime from uber_trips
    where strftime('%s', pickup_datetime) BETWEEN strftime('%s', '2012-10-22') AND strftime('%s', '2012-11-06')
),
trip_aggr as (
    select strftime('%Y-%m-%d:%H', pickup_datetime) as day_hour, count(1) as heat
    from all_trip
    group by strftime('%Y-%m-%d:%H', pickup_datetime)
)
select day_hour, heat, coalesce(HourlyWindSpeed, 0), coalesce(HourlyPrecipitation,0)
from trip_aggr
left join hourly_weather
on trip_aggr.day_hour = strftime('%Y-%m-%d:%H', hourly_weather.daytime)
