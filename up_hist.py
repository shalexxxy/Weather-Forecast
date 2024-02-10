import pandas as pd
from meteostat import Point, Daily
import time
from datetime import datetime

class Weather_hist:
    def __init__(self):
        self.data_hist = pd.read_csv('data/data_weather.csv')
        self.data_hist = self.data_hist.drop_duplicates()
        self.data_places = pd.read_csv('data/data_places.csv')

    def get_wether(self, point_id, start, end, point):
        data = Daily(point, start, end)
        data = data.fetch().reset_index()
        data = data.rename(columns={'index': 'time'})
        data = data[['time', 'tavg']]
        data['point_id'] = point_id
        return data

    def get_point_id(self, name):
        places = pd.read_csv('data/data_places.csv')
        point_id = places[places['name_ru'].str.contains(name, case = False)]['geonameid'].unique()[0]
        return point_id

    def update_bd(self):
        print('Updating historical data ...')
        max_dates = self.data_hist[['point_id', 'time']].groupby('point_id').max().reset_index()
        max_dates = max_dates.merge(self.data_places, left_on = 'point_id', right_on = 'geonameid', how = 'inner')
        new_data = max_dates.apply(lambda x:
                                   self.get_wether(x['point_id'], x['time'],   datetime.now(), Point(x['lat'], x['long']) ) , axis = 1)

        return pd.concat(list(new_data))


