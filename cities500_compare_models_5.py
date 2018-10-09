from sklearn.datasets import make_friedman1
from sklearn import metrics  
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.linear_model import Lasso, LassoCV
from sklearn.linear_model import ElasticNet, ElasticNetCV
from sklearn.linear_model import Lars, LassoLars, LassoLarsCV
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import statsmodels.formula.api as sm
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_validate
from sklearn.datasets import make_classification
import pandas as pd
import numpy as np
import missingno as mn
import seaborn as sns
import statsmodels.formula.api as smf
from statsmodels.tools.tools import add_constant
from statsmodels.stats.diagnostic import het_goldfeldquandt
from statsmodels.stats.outliers_influence import variance_inflation_factor


df = pd.read_csv('data/Clean_data_w_state.csv')
df.rename(columns={'Income_to_pov_rat_lt_1.5' : 'Income_to_pov_rat_lt_15'}, inplace=True)
y = df['Data_Value'].values
X = df.drop(['Data_Value'], axis=1).values

all_cols = list(df.columns)
all_cols.remove('Data_Value')
all_columns = "+".join(all_cols)
my_formula = "y~" + all_columns
results1 = smf.ols(my_formula, data=df).fit()
print(results1.summary2())

f_stat, p_val, inc_dec = het_goldfeldquandt(results1.resid, results1.model.exog)
print(f'For model 1 het goldfeldquandt test, the f stat is {f_stat} and the p value is {p_val}')

vif_df = add_constant(df.drop(['Data_Value'], axis=1))
vifs = pd.Series([variance_inflation_factor(vif_df.values, i) 
               for i in range(vif_df.shape[1])], 
              index=vif_df.columns)
print(vifs)


X_train, X_test, y_train, y_test = train_test_split(X, y)
model = LinearRegression()
model.fit(X_train, y_train)
pred_y = model.predict(X_test)
# score = model.score(pred_y, y_test)
# print(score
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, pred_y))  
print('Mean Squared Error:', metrics.mean_squared_error(y_test, pred_y))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, pred_y)))  


# def select_model(X,y,estimators,score_type='neg_mean_squared_log_error',cv=10):
#     estimator_score={}
#     for model in estimators:
#         print(f'Cross validating {model.__class__.__name__}')
#         estimator_score[model.__class__.__name__]=(-1*np.mean((cross_validate(model,X,y,scoring=score_type,cv=cv))['test_score']))**.5
#     return estimator_score

# def tune_model(X,y,model, cv=10):
#     estimator_score={}
#     if model.__class__.__name__ == 'Lasso':
#         lass = LassoCV(n_alphas=200,cv=cv).fit(X,y)
#         best_alpha = lass.alpha_
#     elif model.__class__.__name__ == 'Ridge':
#         alphas = np.logspace(-3,3,200)
#         ridge = RidgeCV(alphas=alphas, cv=cv).fit(X,y)
#         best_alpha = ridge.alpha_
#     elif model.__class__.__name__ == 'ElasticNet':
#         enet = ElasticNetCV(n_alphas=200, cv=cv).fit(X,y)
#         best_alpha = enet.alpha_
#     elif model.__class__.__name__  == 'LassoLars':
#         ll = LassoLarsCV(fit_intercept=True, max_n_alphas=200).fit(X,y)
#         best_alpha = ll.alpha_
#     return best_alpha

# if __name__=='__main__':
#     df = pd.read_csv('../data/impute1.csv')
#     X = df.drop(['SalePrice','saledate'], axis=1).values
#     print('Tuning Ridge')
#     ridge_alpha = tune_model(X,y, Ridge())
#     print(f'Ridge alpha: {ridge_alpha}')
#     print('Tuning Lasso')
#     lasso_alpha = tune_model(X,y, Lasso())
#     print(f'Lasso alpha: {lasso_alpha}')
#     print('Tuning ElasticNet')
#     enet_alpha = tune_model(X,y, ElasticNet())
#     print(f'ElasticNet alpha: {enet_alpha}')
#     print('Tuning LassoLars')
#     ll_alpha = tune_model(X,y, LassoLars())
#     print(f'LassoLars alpha: {ll_alpha}')


#     models=[LinearRegression(),Ridge(alpha = ridge_alpha),
#             Lasso(alpha = lasso_alpha),ElasticNet(alpha=enet_alpha),
#             LassoLars(alpha = ll_alpha)]
#     test_est=select_model(X,y,[models])
#     print(test_est)
#     b=max(test_est).index()
#     best_model=models[b]
#     print(f'Best model is {best_model.__class__.__name__} with an R^2 of {round(test_est[b],3)}')
#     y_act=pd.read_csv('../data/end_of_day/test_actual.csv', usecols='SalePrice').values
