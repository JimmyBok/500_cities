from analyze_data_sklearn import SkLearnResults, init_data
import os
import pandas as pd 
import numpy as np
from tabulate import tabulate 
from sklearn import metrics  
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
import matplotlib.pyplot as plt
from sklearn import linear_model


class RidgeData(SkLearnResults):
    ''' 
    Class to handle data for 500 cities project
        +Will download data into pwd (or other specified dir)
        +Reads in variables from initial data dict
    '''
    def __init__(self, *args, **kwargs):
        super(RidgeData,self).__init__(*args, **kwargs)

    def run_ridge_analysis(self):
        self.load_data()
        self.get_target_predictors()
        self.split_data()
        self.ridge_regression()
        self.plot_alphas()

    def ridge_regression(self):
        print('Running Ridge Regression')
        self.alphas = np.logspace(-3,3,200)
        self.ridge = RidgeCV(alphas=self.alphas, cv=self.cv).fit(self.X_train, self.y_train)
        self.model = Ridge(alpha = self.ridge.alpha_)
        self.fit_and_test_model(self.model, alpha=self.ridge.alpha_)

    def plot_alphas(self):
        self.coefs = []
        for a in self.alphas:
            ridgereg  = linear_model.Ridge(alpha=a, fit_intercept=False)
            ridgereg.fit(self.X_train, self.y_train)
            self.coefs.append(ridgereg.coef_)
        ax = plt.gca()
        ax.plot(self.alphas, self.coefs)
        ax.set_xscale('log')
        ax.set_xlim(ax.get_xlim()[::-1])  # reverse axis
        plt.xlabel('alpha')
        plt.ylabel('weights')
        plt.title('Ridge coefficients as a function of the regularization')
        plt.axis('tight')
        plt.show()
        plt.close()


    def fit_and_test_model(self, model, alpha=None):
        self.model.fit(self.X_train, self.y_train)
        self.train_pred_y = model.predict(self.X_train)
        self.test_pred_y = model.predict(self.X_test)
        self.train_scores=(cross_validate(model,self.X_train,self.y_train,scoring=self.score_type,cv=self.cv))['test_score']
        self.test_scores=(cross_validate(model,self.X_test,self.y_test,scoring=self.score_type,cv=self.cv))['test_score']
        self.train_rmse = np.sqrt(-1*self.train_scores)
        self.test_rmse = np.sqrt(-1*self.test_scores)
        self.test_r2 = metrics.r2_score(self.y_test, self.test_pred_y)

if __name__ == '__main__':
    ridge = RidgeData(init_data)
    ridge.run_ridge_analysis()



