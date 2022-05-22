import pandas as pd
import nsrdb_weather as ns

#####TEST#########
# lat = 39.124227
# long = -121.066468
#
# data = ns.getyear(2020,lat,long)
# df = pd.concat(data['DataFrame'])
#
# # read in date, time, month, day
# df.insert(0, 'DateTime', df.index)
# df.insert(1, 'Date', pd.to_datetime(df['DateTime']).dt.date)
# df.insert(2, 'Time', pd.to_datetime(df['DateTime']).dt.time)
# df.insert(3, 'Month', pd.DatetimeIndex(df['Date']).month)
# df.insert(4, 'Day', pd.DatetimeIndex(df['Date']).day)
# df.insert(5, 'Year', 2020)
#
# # max wind speed by day
# df_new = df.groupby(pd.Grouper(key='Date')).max()
# df_new.insert(0, 'Date', df_new.index)
#
# PGE_2020 = pd.read_csv('PGE_2020.csv')
# PGE_2020 = PGE_2020[['Date', 'Year', 'Month', 'Day', 'Time', 'Latitude', 'Longitude']]
# df_date = PGE_2020[['Month', 'Day', 'Year']]
# PGE_2020['Date']= pd.to_datetime(df_date)
#
# wind_speed_vector = []
# for i in PGE_2020.index:
#     lat = PGE_2020['Latitude'][i]
#     long = PGE_2020['Longitude'][i]
#     date = PGE_2020['Date'][i]
#     date = date.date()
#     wind_speed = df_new.loc[df_new['Date'] == date]['wind_speed[m/s]'].values[0]
#     wind_speed_vector.append(wind_speed)
#
# PGE_2020['Wind Speed'] = wind_speed_vector

PGE = pd.read_csv('PGE_fire_incident_reportsAll.csv')
PGE = PGE[['date', 'year', 'month', 'day', 'time', 'latitude', 'longitude']]
df_date = PGE[['month', 'day', 'year']]
PGE['date']= pd.to_datetime(df_date)

wind_speed_vector = []
for i in PGE.index:
    lat = PGE['latitude'][i]
    long = PGE['longitude'][i]
    year = PGE['year'][i]
    date = PGE['date'][i]
    date = date.date()
    data = ns.getyear(year,lat,long)
    df = pd.concat(data['DataFrame'])
    df.insert(0, 'DateTime', df.index)
    df.insert(1, 'Date', pd.to_datetime(df['DateTime']).dt.date)
    df.insert(2, 'Time', pd.to_datetime(df['DateTime']).dt.time)
    df.insert(3, 'Month', pd.DatetimeIndex(df['Date']).month)
    df.insert(4, 'Day', pd.DatetimeIndex(df['Date']).day)
    df.insert(5, 'Year', year)

    # max wind speed by day
    df_new = df.groupby(pd.Grouper(key='Date')).max()
    df_new.insert(0, 'Date', df_new.index)

    wind_speed = df_new.loc[df_new['Date'] == date]['wind_speed[m/s]'].values[0]
    wind_speed_vector.append(wind_speed)

PGE['Wind Speed'] = wind_speed_vector






