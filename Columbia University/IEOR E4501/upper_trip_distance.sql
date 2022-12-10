
with all_trips as (
    SELECT distance,
        pickup_datetime
    FROM taxi_trips
    where strftime('%Y-%m', pickup_datetime) == "2013-07"
    union all
    SELECT distance,
        pickup_datetime
    FROM uber_trips
    where strftime('%Y-%m', pickup_datetime) == "2013-07"
),
sorted_trips as (
    SELECT distance,
        pickup_datetime,
        ROW_NUMBER() OVER (ORDER BY distance DESC) AS rank
    FROM all_trips
)
select distance from sorted_trips
where rank = (select ROUND((count(1) - 1) * (1 - 0.95)) from sorted_trips where strftime('%Y-%M', pickup_datetime) == "2013-07")
