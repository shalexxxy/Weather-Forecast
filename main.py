import up_hist as us
from feature_preprocessing import  collect_train_features
import datetime
weather = us.Weather_hist()

print(weather.data_hist.head())
train = collect_train_features(weather)
train.to_csv('data/features.csv')