import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def violinplot(x, y, start: int = 0, num_features: int = 10):
  data = pd.concat([y, x.iloc[:, start:num_features]], axis=1)
  data = pd.melt( data, 
                  id_vars="diagnosis",
                  var_name="features",
                  value_name='value')
  plt.figure(figsize=(20, 12))
  sns.violinplot(x="features", y="value", hue="diagnosis", data=data, split=True, inner="quart")
  plt.xticks(rotation=90)
  plt.show()


def boxplot(x, y, start: int = 0, num_features: int = 10):
    data = pd.concat([y, x.iloc[:, start:num_features]], axis=1)
    data = pd.melt(data,
                   id_vars="diagnosis",
                   var_name="features",
                   value_name='value')
    plt.figure(figsize=(20, 12))
    sns.boxplot(x="features", y="value", hue="diagnosis", data=data)
    plt.xticks(rotation=90)
    plt.show()


def swarmplot(x, y, start: int = 0, num_features: int = 10):
    data = pd.concat([y, x.iloc[:, start:num_features]], axis=1)
    data = pd.melt(data,
                   id_vars="diagnosis",
                   var_name="features",
                   value_name='value')
    plt.figure(figsize=(20, 12))
    sns.swarmplot(x="features", y="value", hue="diagnosis", data=data)
    plt.xticks(rotation=90)
    plt.show()


def plot_correlation(x):
  corr = x.corr()
  mask = np.zeros_like(corr, dtype=np.bool)
  mask[np.triu_indices_from(mask)] = True
  cmap = sns.diverging_palette(230, 20, as_cmap=True)
  fig, ax = plt.subplots(figsize=(24, 20))
  heatmap = sns.heatmap(corr, mask=mask, square=True, linewidths=.5,
                        vmin=-1, vmax=1, cmap='coolwarm', annot=True, fmt='.1f')
  heatmap.set_title('Correlation between features',
                    fontdict={'fontsize': 15}, pad=12)
  fig.show()


def pairplot(x, y, cols):
  data = x[cols]
  data["diagnosis"] = y
  g = sns.PairGrid(data, hue="diagnosis")
  g.map_diag(sns.histplot)
  g.map_offdiag(sns.scatterplot)
  g.map_lower(sns.kdeplot, cmap="Blues_d")
  g.map_upper(plt.scatter)
  g.map_diag(sns.kdeplot, lw=3)
  g.add_legend()
  plt.show()
