import pandas as pd
from log import get_logger

my_logger = get_logger("DfOverview")
my_logger.debug("Loaded successfully!")


class DfOverview:
  """
      Give an overview for a given data frame, 
      like null persentage for each columns, 
      unique value percentage for each columns and more
  """

  def __init__(self, df: pd.DataFrame) -> None:
    self.df = df

  def missing_value(self) -> None:
    nullSum = self.df.isna().sum()
    return [col for col in nullSum]

  def unique_values(self) -> None:
    return [self.getUniqueCount(column) for column in self.df]

  def percentage(self, list):
    return [str(round(((value / self.df.shape[0]) * 100), 2)) + '%' for value in list]

  def getOverview(self) -> None:

    _labels = [column for column in self.df]  # Only numeric columns
    _count = self.df.count().values
    _unique = [self.df[column].value_counts().shape[0] for column in self.df]
    _missing_values = self.missing_value()

    columns = [
      'label',
      'count',
      'none_count',
      'none_percentage',
      'unique_value_count',
      'unique_percentage',
      'dtype']
    data = zip(
      _labels,
      _count,
      _missing_values,
      self.percentage(_missing_values),
      _unique,
      self.percentage(_unique),
      self.df.dtypes
    )
    new_df = pd.DataFrame(data=data, columns=columns)
    new_df.set_index('label', inplace=True)
    new_df.sort_values(by=["none_count"], inplace=True)
    return new_df
