import pandas as pd
from sklearn.preprocessing import Normalizer, MinMaxScaler


class ScalerNormalizer:
    def __init__(self) -> None:
        pass

    def normalizer(self, df, columns):
        norm = Normalizer()
        return pd.DataFrame(norm.fit_transform(df), columns=columns)

    def scaler(self, df, columns):
        minmax_scaler = MinMaxScaler()
        return pd.DataFrame(minmax_scaler.fit_transform(df), columns=columns)

    def scale_and_normalize(self, df, columns):
        return self.normalizer(self.scaler(df, columns), columns)
