import gzip
import json
import pandas as pd

with gzip.open('daily_14.json.gz', 'rt') as f:
    data = [json.loads(line) for line in f if line.strip()]

print(data[0])

weather = pd.json_normalize(data)
print ('city_records = ', weather.shape[0])

countries_count = weather['city.country'].nunique()
print ('countries_count = ', countries_count)

most_cities_country = weather.groupby('city.country')['city.name'].nunique().sort_values(ascending=False)
print('10 countries have the most cities:', most_cities_country[0:10])

forecasts = weather.explode('data')
print('exploded data rows = ', len(forecasts))

mean_daytime_temp = (
    forecasts.assign(day_temp=forecasts['data'].map(lambda d: d['temp']['day']))
    .groupby('city.name')['day_temp']
    .mean().sort_values(ascending=False)
)
print('top ten hottest cities = ', mean_daytime_temp[0:10])

forecasts['date'] = pd.to_datetime(forecasts['data'].map(lambda d: d['dt']), unit='s')
forecasts['temp_min'] = forecasts['data'].map(lambda d: d['temp']['min'])
forecasts['temp_max'] = forecasts['data'].map(lambda d: d['temp']['max'])
forecasts['humidity'] = forecasts['data'].map(lambda d: d['humidity'])
forecasts['weather_description'] = forecasts['data'].map(lambda d: d['weather'][0]['description'])

SF_data = forecasts.loc[
    forecasts['city.name'] == 'San Francisco',
    ['date', 'temp_min', 'temp_max', 'humidity', 'weather_description'],
]
print(SF_data)

