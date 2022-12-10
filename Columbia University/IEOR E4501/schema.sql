
CREATE TABLE hourly_weather(
   daytime datetime PRIMARY KEY,
   HourlyWindSpeed FLOAT,
   HourlyPrecipitation FLOAT
);

CREATE TABLE daily_weather(
   daytime datetime PRIMARY KEY,
   DailyWindSpeed FLOAT,
   DailyPrecipitation FLOAT
);

CREATE TABLE taxi_trips(
   trip_id int PRIMARY KEY,
   pickup_datetime timestamp,
   tip_amount FLOAT,
   pickup_longitude DOUBLE,
   pickup_latitude DOUBLE,
   dropoff_longitude DOUBLE,
   dropoff_latitude DOUBLE,
   distance DOUBLE
);

CREATE TABLE uber_trips(
   trip_id int PRIMARY KEY,
   pickup_datetime timestamp,
   pickup_longitude DOUBLE,
   pickup_latitude DOUBLE,
   dropoff_longitude DOUBLE,
   dropoff_latitude DOUBLE,
   distance DOUBLE
);
