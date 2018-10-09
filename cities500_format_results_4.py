import os
import datetime
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
from tabulate import tabulate
import matplotlib as mpl
mpl.rcParams.update({
    'font.size'           : 20.0,
    'axes.titlesize'      : 'large',
    'axes.labelsize'      : 'medium',
    'xtick.labelsize'     : 'medium',
    'ytick.labelsize'     : 'medium',
    'legend.fontsize'     : 'large',
})
# Get pwd to set as home for project
home = os.getcwd() + '/'
time = datetime.datetime.now() # Write outputs with date/time to avoid overwriting outputs
date_str = time.strftime("%Y_%m_%d")
#Set up variables in dict to pass to class
initial_data = {
    'home' : home, # Directory for all data and output using pwd
    'date_str' : date_str,
    'time' : time # to clock downloading times
}
# Additonal variables that have to be added once the dict is input
#   Due to referencing other objects in the dict
initial_data['data_dir'] = initial_data['home'] + 'data/' # Where output will be stored
initial_data['merged_csv'] = initial_data['data_dir'] + 'Merged_data_2018_10_06.csv' # original data by tract (to get N)
initial_data['clean_csv'] = initial_data['data_dir'] + 'Clean_data_w_state.csv'
initial_data['df_csvs'] = {'orig' : initial_data['merged_csv'],
                    'data': initial_data['clean_csv']
        }

class Results():
    
    def __init__(self, initial_data):
        '''
        Intialize class object
        PARAMETERS
        ----------
        initial_data : dict
            Contains keyword variables include directory location, data url
        RETURNS
        -------
        None
        '''
        for key in initial_data:
            setattr(self, key, initial_data[key])

    def load_data(self):
        for key in self.df_csvs:
            setattr(self, key, pd.read_csv(self.df_csvs[key]))

    def lost_data(self):
        temp = pd.Series()
        temp['Initial'] = len(self.orig)
        temp['Final'] = len(self.data)
        temp['Dropped'] = temp['Initial'] - temp['Final']
        temp['Dropped %'] = (temp['Dropped'] / temp['Initial'])*100
        self.total_dropped = temp.to_frame().transpose()
        self.to_markdown(self.total_dropped, round_places=3)

    def to_markdown(self, df, round_places=3):
        """Returns a markdown, rounded representation of a dataframe"""
        print(tabulate(df.round(round_places), headers='keys', tablefmt='pipe', showindex=False))
        
    def box_plot_vars(self, df, var_list, name='boxplot', xrot =0 ):
        plt.figure(figsize=(20,10))
        df[var_list].boxplot(rot=xrot)
        # ax.xaxis.set_tick_params(rotation=xrot)
        plt.tight_layout()
        # plt.show()
        plt.savefig('./images/'+name+'.png')
        plt.close()

    def state_data(self):
        state_vars = [ x for x in self.data.columns if x.startswith('State')]
        self.states = self.data[state_vars]
        self.states['State_Abbr_CO']=self.states[state_vars].apply(lambda row: 1 if row.sum()==0 else 0, axis=1)
        self.states_sum = self.states.sum()
        ax = self.states_sum.plot.box()
        ax.set_xticklabels(['Count'])
        plt.tight_layout()
        # plt.show()
        plt.savefig('./images/State_count.png')
        plt.close()

if __name__ == '__main__':
    results = Results(initial_data)
    results.load_data()
    results.lost_data()
    var_list = [['Data_Value'], ['Med_age'], ['Percent_female', 'Edu_less_than_hs_or_GED',
       'Income_to_pov_rat_lt_1.5', 'Commute_time_lt_30',
       'Work_depart_before_8am', 'Percent_insured']]
    img_names =['Binge_drinking', 'Median_Age', 'Demographic_percentages']
    rotations = [0, 0, 15]
    for variables, names, rot in zip(var_list, img_names, rotations):
        results.box_plot_vars(results.data, variables, name=names, xrot=rot)
    results.state_data()
