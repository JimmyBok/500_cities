import os
import pandas as pd 
import numpy as np
from tabulate import tabulate 
from sklearn import metrics  
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.linear_model import Lasso, LassoCV
from sklearn.linear_model import ElasticNet, ElasticNetCV
from sklearn.linear_model import Lars, LassoLars, LassoLarsCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate

# Get pwd to set as home for project
home = os.getcwd() + '/' # where we are,
img_dir = home + '../images/' # where images live
data_dir = home + '../data/' # where data live
merged_csv = data_dir + 'Merged_data.csv' # original data by tract (to get N)
clean_csv = data_dir + 'Clean_data_w_state.csv' # cleaned data to analyze
#create dict to pass variables names to class
init_data = {'home' : home,
                'img_dir' : img_dir, 
                'data_dir' : data_dir,
                'merged_csv' : merged_csv,
                'clean_csv' : clean_csv,
                'cv' : 10, 
                'random_seed': 42,
                'score_type': 'neg_mean_squared_error',
                'results' : pd.DataFrame()
                }

init_data['df_csvs'] = {'orig' : init_data['merged_csv'],
                            'data': init_data['clean_csv']
                        }

class SkLearnResults():
    
    def __init__(self, init_data):
        for key in init_data:
            setattr(self, key, init_data[key])

    def run_sk_analysis(self):
        self.load_data()
        self.get_target_predictors()
        self.split_data()
        self.linear_regression()
        self.lasso_regression()
        self.ridge_regression()
        self.enet_regression()
        self.lasso_lars_regression()
        self.clean_results_table()

    def load_data(self):
        for key in self.df_csvs:
            setattr(self, key, pd.read_csv(self.df_csvs[key]))

    def get_target_predictors(self):
        df = self.data
        self.X = df.drop(['Data_Value'], axis=1).values
        self.feature_names = df.drop(['Data_Value'], axis=1).columns
        self.y = df['Data_Value'].values

    def split_data(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, random_state=self.random_seed)

    def linear_regression(self):
        print('Running Linear Regression')
        model = LinearRegression()
        self.fit_and_test_model(model)

    def lasso_regression(self):
        print('Running Lasso Regression')
        lass = LassoCV(n_alphas=200,cv=self.cv).fit(self.X_train,self.y_train)
        model = Lasso(alpha = lass.alpha_)
        self.fit_and_test_model(model, alpha=lass.alpha_)

    def ridge_regression(self):
        print('Running Ridge Regression')
        alphas = np.logspace(-3,3,200)
        ridge = RidgeCV(alphas=alphas, cv=self.cv).fit(self.X_train, self.y_train)
        model = Ridge(alpha = ridge.alpha_)
        self.fit_and_test_model(model, alpha=ridge.alpha_)

    def enet_regression(self):
        print('Running Elastic Net Regression')
        enet = ElasticNetCV(n_alphas=200, cv=self.cv).fit(self.X_train,self.y_train)
        model = ElasticNet(alpha=enet.alpha_)
        self.fit_and_test_model(model, alpha=enet.alpha_)

    def lasso_lars_regression(self):
        print('Running Lasso Lars Regression')
        ll = LassoLarsCV(fit_intercept=True, max_n_alphas=200).fit(self.X_train,self.y_train)
        model = LassoLars(alpha = ll.alpha_)
        self.fit_and_test_model(model, alpha=ll.alpha_)

    def fit_and_test_model(self, model, alpha=None):
        results_ser = pd.Series()
        results_ser['Model'] = model.__class__.__name__
        results_ser['alpha'] = alpha
        model.fit(self.X_train, self.y_train)
        train_pred_y = model.predict(self.X_train)
        test_pred_y = model.predict(self.X_test)
        train_scores=(cross_validate(model,self.X_train,self.y_train,scoring=self.score_type,cv=self.cv))['test_score']
        test_scores=(cross_validate(model,self.X_test,self.y_test,scoring=self.score_type,cv=self.cv))['test_score']
        train_rmse = np.sqrt(-1*train_scores)
        test_rmse = np.sqrt(-1*test_scores)
        results_ser['train_scores_rmse'] = train_rmse
        results_ser['test_scores_rmse'] = test_rmse
        results_ser['train_mean_rmse'] = train_rmse.mean()
        results_ser['test_mean_rmse'] = test_rmse.mean() 
        test_r2 = metrics.r2_score(self.y_test, test_pred_y)
        results_ser['test_r2'] = test_r2
        self.results = self.results.append(results_ser, ignore_index=True)

    def clean_results_table(self):
        cols_to_keep = ['Model', 'alpha', 'test_mean_rmse', 'test_r2','train_mean_rmse']
        temp = self.results[cols_to_keep]
        self.to_markdown(temp)

    def to_markdown(self, df, round_places=3):
        """Returns a markdown, rounded representation of a dataframe"""
        print(tabulate(df.round(round_places), headers='keys', tablefmt='pipe', showindex=False))

if __name__ =='__main__':
    skresults = SkLearnResults(init_data)
    skresults.run_sk_analysis()
