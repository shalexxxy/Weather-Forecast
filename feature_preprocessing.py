import pandas as pd
import numpy as np
import datetime
import up_hist
import up_hist as uh



def collect_train_features(weather : uh.Weather_hist, date_trashold = None, drop_na_target = True):
    weather.data_hist = weather.data_hist.sort_values(by=['point_id', 'time'])
    weather.data_places = weather.data_places[
        weather.data_places['geonameid'].isin(list(weather.data_hist.point_id.unique()))]
    weather.data_hist['time'] = pd.to_datetime(weather.data_hist['time'])
    if date_trashold is not None:
        sample_data = weather.data_hist[weather.data_hist['time'] > date_trashold]
    else:
        sample_data = weather.data_hist
    for lag in range(7):
        sample_data[f"tavg_{lag}"] = sample_data['tavg'].shift(lag + 1)
        sample_data[f"point_{lag}"] = sample_data['point_id'].shift(lag + 1)
        sample_data[f"tavg_{lag}"] = sample_data.apply(
            lambda x: x[f"tavg_{lag}"] if x['point_id'] == x[f"point_{lag}"] else np.nan, axis=1)
    sample_data = sample_data[['time', 'tavg', 'point_id'] + [f"tavg_{lag}" for lag in range(7)]]
    if drop_na_target == True:
        sample_data = sample_data[~sample_data['tavg'].isna()]
    points_features = weather.data_places[['geonameid', 'lat', 'elev', 'long', 'gtopo']]
    points_features = points_features.rename(columns = {'geonameid' : 'point_id'})
    sample_data = sample_data.merge(points_features, on = 'point_id')
    return sample_data
