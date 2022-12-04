
CREATE TABLE hourly_weather(
   DATE timestamp PRIMARY KEY,
   HourlyWindSpeed FLOAT,
   HourlyPrecipitation FLOAT
);

CREATE TABLE daily_weather(
   DATE timestamp PRIMARY KEY,
   DailyWindSpeed FLOAT,
   DailyPrecipitation FLOAT
);

CREATE TABLE taxis_trips(
   pickup_datetime timestamp,
   tip_amount FLOAT,
   pickup_longitude DOUBLE,
   pickup_latitude DOUBLE,
   dropoff_longitude DOUBLE,
   dropoff_latitude DOUBLE,
   distance DOUBLE
);

CREATE TABLE uber_trips(
   pickup_datetime timestamp,
   pickup_longitude DOUBLE,
   pickup_latitude DOUBLE,
   dropoff_longitude DOUBLE,
   dropoff_latitude DOUBLE,
   distance DOUBLE
);
