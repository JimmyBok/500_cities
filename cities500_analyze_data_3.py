import os
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.diagnostic import het_goldfeldquandt
from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression, LinearRegression
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import metrics  
from statsmodels.tools.tools import add_constant

if not os.path.isdir('./images_w_state'):
    os.makedirs('./images_w_state')

df = pd.read_csv('data/Clean_data_w_state.csv')
df.rename(columns={'Income_to_pov_rat_lt_1.5' : 'Income_to_pov_rat_lt_15'}, inplace=True)
y = df['Data_Value'].values
X = df.drop(['Data_Value'], axis=1).values
# plt.figure(figsize=(20,10))
# pd.plotting.scatter_matrix(df)
# plt.tight_layout()
# # plt.show()
# plt.savefig('./images_w_state/scatter_matrix.png')
# plt.close()
# plt.figure(figsize=(20,10))
# df.boxplot()
# plt.tight_layout()
# # plt.show()
# plt.savefig('./images_w_state/boxplots.png')
# plt.close()
# plt.figure(figsize=(20,10))
# sns.pairplot(df)
# plt.tight_layout()
# plt.savefig('./images_w_state/pairplot.png')
# plt.close()

all_cols = list(df.columns)
all_cols.remove('Data_Value')
all_columns = "+".join(all_cols)
my_formula = "y~" + all_columns
results1 = smf.ols(my_formula, data=df).fit()
print(results1.summary2())

# print('Calculating residuals. May take some time...')
# # Takes lots of time. Uncomment when new data included 
# resid_stud1 = results1.outlier_test()['student_resid']
# dev_null1 = sm.graphics.qqplot(resid_stud1, line='45', fit=True)
# plt.tight_layout()
# plt.savefig('./images_w_state/qqplot.png')
# # plt.show()
# plt.close()

# plt.scatter(results1.fittedvalues, results1.resid)
# plt.tight_layout()
# plt.savefig('./images_w_state/resid_scatter.png')
# # plt.show()
# plt.close()

f_stat, p_val, inc_dec = het_goldfeldquandt(results1.resid, results1.model.exog)
print(f'For model 1 het goldfeldquandt test, the f stat is {f_stat} and the p value is {p_val}')

X_train, X_test, y_train, y_test = train_test_split(X, y)
model = LinearRegression()
model.fit(X_train, y_train)
pred_y = model.predict(X_test)
# score = model.score(pred_y, y_test)
# print(score
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, pred_y))  
print('Mean Squared Error:', metrics.mean_squared_error(y_test, pred_y))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, pred_y)))  


vif_df = add_constant(df.drop(['Data_Value'], axis=1))
vifs = pd.Series([variance_inflation_factor(vif_df.values, i) 
               for i in range(vif_df.shape[1])], 
              index=vif_df.columns)
print(vifs)