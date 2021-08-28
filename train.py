
from scripts.ScalerNormalizer import ScalerNormalizer
from scripts.df_overview import DfOverview
from scripts.eda_helper import Helper
import scripts.vis_seaborn as vs
from scripts.file_handler import FileHandler
from causalnex.discretiser.discretiser_strategy import (
    DecisionTreeSupervisedDiscretiserMethod)
from sklearn.metrics import recall_score, f1_score, accuracy_score, precision_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from causalnex.structure.notears import from_pandas, from_pandas_lasso
from causalnex.utils.network_utils import get_markov_blanket
from causalnex.structure.notears import from_pandas
from causalnex.network.sklearn import BayesianNetworkClassifier
from causalnex.network import BayesianNetwork
from causalnex.inference import InferenceEngine
from causalnex.structure import DAGRegressor
from causalnex.discretiser import Discretiser

import os
import sys
sys.path.append(os.path.abspath(os.path.join('../scripts')))


def save_metrics(metrics_obj, path="./metrics.txt"):
    try:
        recall = metrics_obj['Recall']
        F1 = metrics_obj['F1']
        Accuracy = metrics_obj['Accuracy']
        Precision = metrics_obj['Precision']

        fileObj = open(path, "w")
        metrics = [f"Recall: {recall:.2f}\n",
                   f"F1: {F1:.2f}\n", f"Accuracy: {Accuracy:.2f}\n", f"Precision: {Precision:.2f}\n"]
        fileObj.writelines(metrics)
        fileObj.close()
    except:
        fileObj.close()


if __name__ == "__main__":

    helper = Helper()
    fh = FileHandler()

    feat = ['diagnosis', 'perimeter_worst', 'area_worst', 'radius_worst', 'concave points_worst', 'concave points_mean', 'perimeter_mean', 'area_mean', 'radius_mean', 'area_se', 'concavity_mean', 'concavity_worst', 'perimeter_se', 'radius_se', 'compactness_worst', 'compactness_mean',
            'texture_worst', 'concave points_se', 'smoothness_worst', 'texture_mean', 'symmetry_worst', 'concavity_se', 'smoothness_mean', 'symmetry_mean', 'compactness_se', 'fractal_dimension_worst', 'fractal_dimension_se', 'texture_se', 'fractal_dimension_mean', 'symmetry_se', 'smoothness_se']

    df = fh.read_csv("./data/cleaned_data.csv")
    x = df[feat[:29]]

    x['diagnosis'] = x['diagnosis'].apply(lambda x: 1 if x == "M" else 0)
    features = x.iloc[:, 1:]

    sn = ScalerNormalizer()

    normal_data = sn.scale_and_normalize(features, features.columns.to_list())
    normal_data.insert(loc=0, column='diagnosis', value=x['diagnosis'])

    x_selected = normal_data.iloc[:, :10]

    sm = from_pandas(x_selected, tabu_parent_nodes=['diagnosis'],)
    sm.remove_edges_below_threshold(0.8)
    sm = sm.get_largest_subgraph()
    vs.vis_sm(sm)

    bn = BayesianNetwork(sm)
    blanket = get_markov_blanket(bn, 'diagnosis')
    edge_list = list(blanket.structure.edges)

    x_selected = x.iloc[:, :10]
    features = list(x_selected.columns.difference(['diagnosis']))

    tree_discretiser = DecisionTreeSupervisedDiscretiserMethod(
        mode='single',
        tree_params={'max_depth': 3, 'random_state': 27},
    )

    tree_discretiser.fit(
        feat_names=features,
        dataframe=x,
        target_continuous=True,
        target='diagnosis',
    )

    discretised_data = x_selected.copy()

    for col in features:
        discretised_data[col] = tree_discretiser.transform(x_selected[[col]])

    train, test = train_test_split(
        discretised_data, train_size=0.8, test_size=0.2, random_state=27)

    bn = BayesianNetwork(blanket.structure)
    bn = bn.fit_node_states(discretised_data)
    bn = bn.fit_cpds(train, method="BayesianEstimator", bayes_prior="K2")

    pred = bn.predict(test, 'diagnosis')
    true = test['diagnosis']

    metrics = {"Recall": recall_score(y_true=true, y_pred=pred), "F1": f1_score(y_true=true, y_pred=pred), "Accuracy":
               accuracy_score(y_true=true, y_pred=pred), "Precision": precision_score(y_true=true, y_pred=pred)}
    
    save_metrics(metrics)

    print('Recall: {:.2f}'.format(recall_score(y_true=true, y_pred=pred)))
    print('F1: {:.2f} '.format(f1_score(y_true=true, y_pred=pred)))
    print('Accuracy: {:.2f} '.format(accuracy_score(y_true=true, y_pred=pred)))
    print('Precision: {:.2f} '.format(
        precision_score(y_true=true, y_pred=pred)))
