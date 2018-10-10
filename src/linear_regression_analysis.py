from analyze_data_sklearn import SkLearnResults, init_data
import os
import pandas as pd 
import numpy as np
from tabulate import tabulate 
from sklearn import metrics  
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
import matplotlib.pyplot as plt
from sklearn import linear_model
# importing all necessary libraries 
import plotly.plotly as py 
import plotly.graph_objs as go 
import pandas as pd 
import plotly
# some more libraries to plot graph 
import plotly.offline as offline
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot, plot 
  
# To establish connection 
offline.init_notebook_mode(connected=True) 
  


class LinearData(SkLearnResults):
    ''' 
    Class to handle data for 500 cities project
        +Will download data into pwd (or other specified dir)
        +Reads in variables from initial data dict
    '''
    def __init__(self, *args, **kwargs):
        super(LinearData,self).__init__(*args, **kwargs)

    def run_linear_analysis(self):
        self.load_data()
        self.get_target_predictors()
        self.split_data()
        self.linear_regression()
        self.create_df_w_name_coef()
        self.create_table_of_demos()
        self.plot_state_coeffs()

    def linear_regression(self):
        print('Running Linear Regression')
        self.model = LinearRegression()
        self.fit_and_test_model()

    def fit_and_test_model(self):
        self.model.fit(self.X_train, self.y_train)
        self.train_pred_y = self.model.predict(self.X_train)
        self.test_pred_y = self.model.predict(self.X_test)
        self.train_scores=(cross_validate(self.model,self.X_train,self.y_train,scoring=self.score_type,cv=self.cv))['test_score']
        self.test_scores=(cross_validate(self.model,self.X_test,self.y_test,scoring=self.score_type,cv=self.cv))['test_score']
        self.train_rmse = np.sqrt(-1*self.train_scores)
        self.test_rmse = np.sqrt(-1*self.test_scores)
        self.test_r2 = metrics.r2_score(self.y_test, self.test_pred_y)

    def create_df_w_name_coef(self):
        feature_dict = {'name' : lrd.feature_names,
                        'coef' : lrd.model.coef_
                        }
        self.coeff_df = pd.DataFrame.from_dict(feature_dict)
        ser = pd.Series({'name':'Intercept', 'coef': lrd.model.intercept_})
        self.coeff_df = self.coeff_df.append(ser, ignore_index=True)
        ser = pd.Series({'name':'StateAbbr_CO', 'coef': 0})
        self.coeff_df = self.coeff_df.append(ser, ignore_index=True)
        self.state_df = self.coeff_df[self.coeff_df['name'].str.match('StateAbbr_')]
        self.demo_df = self.coeff_df[~self.coeff_df['name'].str.match('StateAbbr_')]

    def create_table_of_demos(self):
        self.demo_df = self.demo_df.T
        self.demo_df.columns = self.demo_df.iloc[0]
        self.demo_df.reset_index(inplace=True)
        self.demo_df.drop(self.demo_df.index[0], inplace=True)
        vois = ['Intercept', 'Percent_female', 'Income_to_pov_rat_lt_1_5',
                'Edu_less_than_hs_or_GED', 'Percent_insured', 'Work_depart_before_8am',
                'Med_age', 'Commute_time_lt_30'
                ]
        self.to_markdown(self.demo_df[vois])
        
    def plot_state_coeffs(self):
        self.state_df['State'] = self.state_df['name'].apply(lambda x: x[-2:])
        self.state_df['Coef_str'] = self.state_df['coef'].apply(lambda x: '{:,.2%}'.format(x))
        # type defined is choropleth to 
        # plot geographical plots 
        data = dict(type = 'choropleth', 
                    # location: Arizoana, California, Newyork 
                    locations = self.state_df['State'].values, 
                    # States of USA 
                    locationmode = 'USA-states', 
                    # colorscale can be added as per requirement 
                    colorscale = 'Jet', 
                    # text can be given anything you like 
                    text = self.state_df['Coef_str'].values, 
                    z = self.state_df.coef.values, 
                    colorbar = {'title': 'Impact of State on Binge Drinking'}) 
        layout = dict(geo ={'scope': 'usa'})           
        # passing data dictionary as a list  
        choromap = go.Figure(data = [data], layout = layout) 
        # plotting graph 
        offline.iplot(choromap, image='png')
        plotly.io.write_image(choromap, '../images/choromap.png') 

        
if __name__ == '__main__':
    lrd = LinearData(init_data)
    lrd.run_linear_analysis()



