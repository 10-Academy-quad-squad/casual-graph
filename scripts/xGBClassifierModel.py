import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import GradientBoostingClassifier

# from app_logger import App_Logger


def loss_function(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    return rmse


class XGBClassifierModel:

    def __init__(self, X_train, X_test, y_train, y_test, max_depth=5):

        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

        self.clf = GradientBoostingClassifier()
        # self.logger = App_Logger("models.log").get_app_logger()

    def train(self, folds=1):

        kf = KFold(n_splits=folds)

        iterator = kf.split(self.X_train)

        loss_arr = []
        acc_arr = []
        # self.logger.info(
        #     f"Model GradientBoostingClassifier training started with k-flod: {folds}")

        for i in range(folds):
            train_index, valid_index = next(iterator)

            X_train, y_train = self.X_train.iloc[train_index], self.y_train.iloc[train_index]
            X_valid, y_valid = self.X_train.iloc[valid_index], self.y_train.iloc[valid_index]

            self.clf = self.clf.fit(X_train, y_train)

            vali_pred = self.clf.predict(X_valid)

            accuracy = self.calculate_score(y_valid, vali_pred)

            loss = loss_function(y_valid, vali_pred)

            self.__printAccuracy(accuracy, i, label="Validation")
            self.__printLoss(loss, i, label="Validation")
            print()

            acc_arr.append(accuracy)
            loss_arr.append(loss)

        return self.clf, acc_arr, loss_arr

    def test(self):

        y_pred = self.clf.predict(self.X_test)

        accuracy = self.calculate_score(y_pred, self.y_test)
        self.__printAccuracy(accuracy, label="Test")

        report = self.report(y_pred, self.y_test)
        matrix = self.confusion_matrix(y_pred, self.y_test)

        loss = loss_function(self.y_test, y_pred)

        return accuracy, loss, report, matrix

    def get_feature_importance(self):
        importance = self.clf.feature_importances_
        fi_df = pd.DataFrame()

        fi_df['features'] = self.X_train.columns.to_list()
        fi_df['importance'] = importance

        return fi_df.sort_values(by="importance", ascending=False)

    def __printAccuracy(self, acc, step=1, label=""):
        # self.logger.info(f"Model GradientBoostingClassifier accuracy: {acc}")
        print(
            f"step {step}: {label} Accuracy of GradientBoostingClassifier is: {acc:.3f}")

    def __printLoss(self, loss, step=1, label=""):
        # self.logger.info(f"Model GradientBoostingClassifier accuracy: {loss}")
        print(
            f"step {step}: {label} Loss of GradientBoostingClassifier is: {loss:.3f}")

    def calculate_score(self, pred, actual):
        return metrics.accuracy_score(actual, pred)

    def report(self, pred, actual):
        print("Test Metrics")
        print("================")
        print(metrics.classification_report(pred, actual))
        return metrics.classification_report(pred, actual)

    def confusion_matrix(self, pred, actual):
        ax = sns.heatmap(pd.DataFrame(metrics.confusion_matrix(pred, actual)))
        plt.title('Confusion matrix')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        return metrics.confusion_matrix(pred, actual)
