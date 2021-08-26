# casual-graph
**Table of Contents**

  - [Overview](#overview)
  - [Project Structure](#project-structure)
    - [data:](#data)
    - [notebooks:](#notebooks)
    - [scripts](#scripts)
    - [tests:](#tests)
    - [logs:](#logs)
    - [root folder](#root-folder)
  - [Installation guide](#installation-guide)

## Overview
- A common frustration in the industry, especially when it comes to getting business insights from tabular data, is that the most interesting questions (from their perspective) are often not answerable with observational data alone. These questions can be similar to:
    - “What will happen if I halve the price of my product?”
    - “Which clients will pay their debts only if I call them?”

- The causal graph is a central object in the framework mentioned above, but it
is often unknown, subject to personal knowledge and bias, or loosely
connected to the available data. The main objective of this task is to
highlight the importance of the matter in a concrete way.

## Project Structure
The repository has a number of files including python scripts, jupyter notebooks, pdfs and text files. Here is their structure with a brief explanation.

## Data
- We extracted the data from [kaggle](https://www.kaggle.com/uciml/breast-cancer-wisconsin-data) or
- from [UCI Machine Learning Repository](https://archive-beta.ics.uci.edu/ml/datasets?name=breast)
## notebooks
- [EDA.ipynb](https://github.com/10-Academy-quad-squad/casual-graph/blob/dev-abreham/notebooks/1.%20EDA.ipynb): a jupyter notebook for exploratory data analysis
## scripts
- [app_logger.py](https://github.com/10-Academy-quad-squad/casual-graph/blob/dev-abreham/scripts/app_logger.py)
    - a python script for logging
- [file_handler.py](https://github.com/10-Academy-quad-squad/casual-graph/blob/dev-abreham/scripts/file_handler.py)

    - a python script for handling reading and writing of csv, pickle and other files
- [config.py](https://github.com/10-Academy-quad-squad/casual-graph/blob/dev-abreham/scripts/config.py)
    - class for exploring the data
- [df_cleaner.py](https://github.com/10-Academy-quad-squad/casual-graph/blob/dev-abreham/scripts/df_cleaner.py)
    - dataframe cleaner helper functions
- [df_outlier.py](https://github.com/10-Academy-quad-squad/casual-graph/blob/dev-abreham/scripts/df_outlier.py)
    - Dataframe Outlier class




