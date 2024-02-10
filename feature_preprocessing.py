import pandas as pd
import numpy as np
import datetime
import up_hist
import up_hist as uh
import time

def collect_train_features(weather : uh.Weather_hist, date_trashold = None, drop_na_target = True):
    print(weather.data_hist.shape)
    start = time.time()
    print('Sorting history weather...')
    weather.data_hist = weather.data_hist.sort_values(by=['point_id', 'time'])
    weather.data_places = weather.data_places[
        weather.data_places['geonameid'].isin(list(weather.data_hist.point_id.unique()))]
    weather.data_hist['time'] = pd.to_datetime(weather.data_hist['time'])
    print('Filtering data by date ...')
    if date_trashold is not None:
        sample_data = weather.data_hist[weather.data_hist['time'] > date_trashold]
    else:
        sample_data = weather.data_hist
    print('Collecting lag features ...')
    for lag in range(7):
        new_sample = sample_data[['time','point_id', 'tavg']].copy()
        new_sample['time'] = new_sample['time'] + datetime.timedelta(days=lag+1)
        new_sample = new_sample.rename(columns={'tavg': f"tavg_{lag+1}"})
        sample_data = sample_data.merge(new_sample, on = ['point_id', 'time'], how = 'left')
    sample_data = sample_data[['time', 'tavg', 'point_id'] + [f"tavg_{lag}" for lag in range(1, 8)]]
    if drop_na_target == True:
        sample_data = sample_data[~sample_data['tavg'].isna()]
    print('adding extra features ...')
    points_features = weather.data_places[['geonameid', 'lat', 'elev', 'long', 'gtopo']]
    points_features = points_features.rename(columns = {'geonameid' : 'point_id'})
    sample_data = sample_data.merge(points_features, on = 'point_id')
    print("time is : ", time.time() - start)
    return sample_data
