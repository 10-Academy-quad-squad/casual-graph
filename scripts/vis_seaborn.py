import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import Markdown, display, Image, display_html


def violinplot(x, y, start: int = 0, num_features: int = 10):
    data = pd.concat([y, x.iloc[:, start:num_features]], axis=1)
    data = pd.melt(data,
                   id_vars="diagnosis",
                   var_name="features",
                   value_name='value')
    plt.figure(figsize=(20, 12))
    sns.violinplot(x="features", y="value", hue="diagnosis",
                   data=data, split=True, inner="quart")
    plt.xticks(rotation=90)
    plt.show()


def plot_count(df: pd.DataFrame, column: str, xcolumn: str = None, ycolumn: str = None) -> None:
    plt.figure(figsize=(12, 7))
    sns.countplot(data=df, x=column)
    plt.title(f'Plot count of {column}', size=18, fontweight='bold')
    if xcolumn:
        plt.xlabel(xcolumn)
    if xcolumn:
        plt.ylabel(ycolumn)
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


def view_df(df, subset=[], color='#66F582'):
    df = df.reset_index()
    style = df.style.set_table_attributes("style='display:inline'").\
        bar(subset=subset, axis=1, color=color)\
        .format({"label": lambda x: x.upper()})\
        .set_properties(**{'background-color': 'white', 'color': 'black'})
    display_html(style._repr_html_(), raw=True)
