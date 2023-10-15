import catboost as ct
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import feature_preprocessing as fp


class BaseModel:
    def __init__(self, load_from_file=False):
        self.model = ct.CatBoostRegressor()
        self.learning_config = {}


    def train(self):
        pass

    def split_data(self):
        pass

    def eval(self):
        pass

    def plot_metrics(self):
        pass
