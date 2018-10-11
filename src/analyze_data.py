import os
import datetime
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt 
import statsmodels.api as sm
import statsmodels.formula.api as smf
from tabulate import tabulate
from statsmodels.tools.tools import add_constant
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_goldfeldquandt

mpl.rcParams.update({
    'font.size'           : 20.0,
    'axes.titlesize'      : 'large',
    'axes.labelsize'      : 'medium',
    'xtick.labelsize'     : 'medium',
    'ytick.labelsize'     : 'medium',
    'legend.fontsize'     : 'large',
})
# Get pwd to set as home for project
home = os.getcwd() + '/' # where we are,
img_dir = home + '../images/' # where images live
data_dir = home + '../data/' # where data live
merged_csv = data_dir + 'Merged_data.csv' # original data by tract (to get N)
clean_csv = data_dir + 'Clean_data_w_state.csv' # cleaned data to analyze
#create dict to pass variables names to class
initial_data = { 'home' : home,
                'img_dir' : img_dir, 
                'data_dir' : data_dir,
                'merged_csv' : merged_csv,
                'clean_csv' : clean_csv
                }
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

    def run_analyze(self):
        self.create_dirs()
        self.load_data()
        self.lost_data()
        var_list = [['Data_Value'], ['Med_age'], ['Percent_female', 'Edu_less_than_hs_or_GED',
            'Income_to_pov_rat_lt_1_5', 'Commute_time_lt_30',
            'Work_depart_before_8am', 'Percent_insured']]
        img_names =['Binge_drinking', 'Median_Age', 'Demographic_percentages']
        rotations = [0, 0, 15]
        for variables, names, rot in zip(var_list, img_names, rotations):
            self.box_plot_vars(self.data, variables, name=names, xrot=rot)
        self.state_data()
        self.run_vif()
        self.run_smf_ols_model()

    def create_dirs(self):
        '''
        Creates directories for 500 cities analysis
            +data dir to store data files (csvs)
        '''
        for mydir in [self.img_dir]:
            self.make_dirs(mydir)

    def make_dirs(self, dirpath):
        if not os.path.isdir(dirpath):
            print(f'Creating directory: {dirpath}')
            os.makedirs(dirpath, exist_ok=True)
        else:
            print(f"Directory exists: {dirpath}")

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
        print("Table for missing data")
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
        plt.savefig(self.img_dir+name+'.png')
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
        plt.savefig(self.img_dir + 'State_count.png')
        plt.close()

    def run_vif(self):
        vif_df = add_constant(self.data.drop(['Data_Value'], axis=1))
        self.vifs = pd.Series([variance_inflation_factor(vif_df.values, i) 
                       for i in range(vif_df.shape[1])], 
                      index=vif_df.columns)
        self.vifs_table = self.vifs.describe().to_frame().transpose()
        print("Table for VIF data")
        self.to_markdown(self.vifs_table)

    def run_smf_ols_model(self):
        self.smf_ols_model()
        # self.smf_ols_qq_plots()
        # self.smf_residual_scatter()
        # self.smf_het_goldfeldquandt()

    def smf_ols_model(self):
        all_cols = list(self.data.columns)
        all_cols.remove('Data_Value')
        all_columns = "+".join(all_cols)
        my_formula = "Data_Value ~" + all_columns
        self.model1 = smf.ols(my_formula, data=self.data).fit()
        print(self.model1.summary2())

    def smf_ols_qq_plots(self):
        # # Takes lots of time. Uncomment when new data included 
        print('Calculating residuals. May take some time...')
        self.resid_stud1 = self.model1.outlier_test()['student_resid']
        dev_null1 = sm.graphics.qqplot(self.resid_stud1, line='45', fit=True)
        plt.tight_layout()
        plt.savefig(self.img_dir + 'qqplot.png')
        plt.close()

    def smf_residual_scatter(self):
        plt.scatter(self.model1.fittedvalues, self.model1.resid)
        plt.tight_layout()
        plt.savefig(self.img_dir + 'resid_scatter.png')
        plt.close()

    def smf_het_goldfeldquandt(self):
        f_stat, p_val, inc_dec = het_goldfeldquandt(self.model1.resid, self.model1.model.exog)
        print(f'For smf model 1 het goldfeldquandt test, the f stat is {f_stat} and the p value is {p_val}')

if __name__ == '__main__':
    results = Results(initial_data)
    results.run_analyze()