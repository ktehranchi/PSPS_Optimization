import pandas as pd
from datetime import datetime, timedelta
from meteostat import Hourly, Point, Stations

#Load Data
PGE = pd.read_csv('Data/PGE_fire_incident_reportsAll.csv')
PGE_vegFire = PGE[PGE.material_at_origin.str.contains('Vegetation') | PGE.contributing_factor.str.contains('High Winds') | PGE.contributing_factor.str.contains('Weather')]
PGE_vegFire['datetime'] = pd.to_datetime(PGE_vegFire[['year','month','day','hour','minute']])

#Import windspeeds
wind_speed_vector = []
wind_speed_max_vector = []

for i in PGE_vegFire.index:
    lat = PGE_vegFire['latitude'][i]
    long = PGE_vegFire['longitude'][i]
    start = PGE_vegFire['datetime'][i]+ timedelta(hours=-5)
    end = PGE_vegFire['datetime'][i] 

    # location = Point(lat, long)
    # # Get hourly data
    # data = Hourly(location, start, end)
    # data = data.fetch()

    stations = Stations()
    stations = stations.nearby(lat,long)
    station = stations.fetch(2)
    data = Hourly(station, start, end)
    data = data.fetch()


    if len(data['wspd'].values) == 0:
        wind_speed = 'no data'
    else:
        data= data.loc[data.index.get_level_values(0)[0]] #filter out the first returned station data
        wind_speed = data.wspd.last('1h')[0]
        wind_speed_max = data.wspd.max()
    wind_speed_vector.append(wind_speed)
    wind_speed_max_vector.append(wind_speed_max)


PGE_vegFire['wind_speed'] = wind_speed_vector
PGE_vegFire['wind_speed_max'] = wind_speed_max_vector
PGE_vegFire.to_csv('Data/PGE_VegFire_windData.csv')


