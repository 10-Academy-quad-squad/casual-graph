import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.model_selection import KFold
import scipy.stats as stat
from sklearn.metrics import mean_squared_error

# from app_logger import App_Logger


def loss_function(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    return rmse


class LogesticRegressionModel:

    def __init__(self, X_train, X_test, y_train, y_test, model_name="LR"):

        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.model_name = model_name

        self.clf = LogisticRegression()
        # self.logger = App_Logger("models.log").get_app_logger()

    def train(self, folds=1):

        kf = KFold(n_splits=folds)

        iterator = kf.split(self.X_train)

        loss_arr = []
        acc_arr = []
        model_name = self.model_name
#         mlflow.end_run()
        # self.logger.info(
        #     f"Model LogisticRegression training started with kflod: {folds}")

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

        accuracy = self.calculate_score(self.y_test, y_pred)
        self.__printAccuracy(accuracy, label="Test")

        report = self.report(y_pred, self.y_test)
        matrix = self.confusion_matrix(y_pred, self.y_test)
        loss = loss_function(self.y_test, y_pred)

        return accuracy, loss, report, matrix

    def __printAccuracy(self, acc, step=1, label=""):
        # self.logger.info(f"Model LogisticRegression accuracy: {acc}")
        print(
            f"step {step}: {label} Accuracy of LogesticRegression is: {acc:.3f}")

    def __printLoss(self, loss, step=1, label=""):
        # self.logger.info(f"Model LogisticRegression loss: {loss}")
        print(f"step {step}: {label} Loss of LogesticRegression is: {loss:.3f}")

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

    def get_p_values(self):
        """ 
        Calcualting p_values for logestic regression.
        code refered from the following link
        https://gist.github.com/rspeare/77061e6e317896be29c6de9a85db301d

        """
        denom = (2.0 * (1.0 + np.cosh(self.clf.decision_function(self.X_train))))
        denom = np.tile(denom, (self.X_train.shape[1], 1)).T
        # Fisher Information Matrix
        F_ij = np.dot((self.X_train / denom).T, self.X_train)
        Cramer_Rao = np.linalg.inv(F_ij)  # Inverse Information Matrix
        sigma_estimates = np.sqrt(np.diagonal(Cramer_Rao))
        z_scores = self.clf.coef_[0] / sigma_estimates  # z-score
        # two tailed test for p-values
        p_values = [stat.norm.sf(abs(x)) for x in z_scores]

        p_df = pd.DataFrame()
        p_df['features'] = self.X_train.columns.to_list()
        p_df['p_values'] = p_values

    def plot_pvalues(self, p_df):

        fig, ax = plt.subplots(figsize=(12, 7))

        ax.plot([0.05, 0.05], [0.05, 5])
        sns.scatterplot(data=p_df, y='features', x='p_values', color="green")
        plt.title("P values of features", size=20)

        plt.xticks(np.arange(0, max(p_df['p_values']) + 0.05, 0.05))

        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

        plt.show()
        return fig

    def feat_importance(self):
        denom = (2.0 * (1.0 + np.cosh(self.clf.decision_function(self.X_train))))
        denom = np.tile(denom, (self.X_train.shape[1], 1)).T
        # Fisher Information Matrix
        F_ij = np.dot((self.X_train / denom).T, self.X_train)
        Cramer_Rao = np.linalg.inv(F_ij)  # Inverse Information Matrix
        sigma_estimates = np.sqrt(np.diagonal(Cramer_Rao))

        feat_importance = self.clf.coef_[0]

        f_df = pd.DataFrame()
        f_df['features'] = self.X_train.columns.to_list()
        f_df['importance'] = feat_importance

        return f_df.sort_values(by="importance", ascending=False)
