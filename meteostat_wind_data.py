import pandas as pd

# Import Meteostat library and dependencies
from datetime import datetime
from meteostat import Hourly, Point

# ############TEST#####################
# # Set time period
# start = datetime(2020, 12, 22, 10, 0)
# #end = datetime(2018, 12, 31, 23, 59)
# end = datetime(2020, 12, 22, 11, 0)
# vancouver = Point(39.16631,-122.142)
# # Get hourly data
# data = Hourly(vancouver, start, end)
# data = data.fetch()
# #
# # Print DataFrame
# print(data)



#########################
PGE = pd.read_csv('PGE_fire_incident_reportsAll.csv')
PGE = PGE[['date', 'year', 'month', 'day', 'time', 'hour', 'minute', 'latitude', 'longitude']]
df_date = PGE[['month', 'day', 'year']]
PGE['date']= pd.to_datetime(df_date)

wind_speed_vector = []
for i in PGE.index:
    lat = PGE['latitude'][i]
    long = PGE['longitude'][i]
    year = PGE['year'][i]
    month = PGE['month'][i]
    day = PGE['day'][i]
    date = PGE['date'][i]
    hour = PGE['hour'][i]
    minute = PGE['minute'][i]

    start = datetime(year, month, day, hour, 0)
    end = datetime(year, month, day, hour, 0)
    location = Point(lat, long)
    # Get hourly data
    data = Hourly(location, start, end)
    data = data.fetch()
    if len(data['wspd'].values) == 0:
        wind_speed = 'no data'
    else:
        wind_speed = data['wspd'].values[0]
    wind_speed_vector.append(wind_speed)


PGE['Wind Speed'] = wind_speed_vector
PGE.to_csv('PGE_new.csv')