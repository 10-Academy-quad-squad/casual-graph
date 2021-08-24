import numpy as np
import pandas as pd
from sklearn.preprocessing import Normalizer, MinMaxScaler
import pickle

from app_logger import App_Logger


class Helper:

    def __init__(self):
        self.logger = App_Logger("helper.log").get_app_logger()

    def percent_missing(self, df: pd.DataFrame) -> float:

        totalCells = np.product(df.shape)
        missingCount = df.isnull().sum()
        totalMissing = missingCount.sum()
        return round((totalMissing / totalCells) * 100, 2)

    def percent_missing_for_col(self, df: pd.DataFrame, col_name: str) -> float:
        total_count = len(df[col_name])
        if total_count <= 0:
            return 0.0
        missing_count = df[col_name].isnull().sum()

        return round((missing_count / total_count) * 100, 2)

    def normalizer(self, df, columns):
        norm = Normalizer()
        return pd.DataFrame(norm.fit_transform(df), columns=columns)

    def scaler(self, df, columns):
        minmax_scaler = MinMaxScaler()
        return pd.DataFrame(minmax_scaler.fit_transform(df), columns=columns)

    def scale_and_normalize(self, df, columns):
        return self.normalizer(self.scaler(df, columns), columns)
