import os
import datetime
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
# Get pwd to set as home for project
home = os.getcwd() + '/'
time = datetime.datetime.now() # Write outputs with date/time to avoid overwriting outputs
date_str = time.strftime("%Y_%m_%d")
#Set up variables in dict to pass to class
initial_data = {
    'home' : home, # Directory for all data and output using pwd
    'date_str' : date_str,
    'time' : time, # to clock downloading times
}
# Additonal variables that have to be added once the dict is input
#   Due to referencing other objects in the dict
initial_data['data_dir'] = initial_data['home'] + 'data/' # Where output will be stored
initial_data['merged_csv'] = initial_data['data_dir'] + 'Merged_data_2018_10_06.csv' # name of merged dataframe
initial_data['clean_csv'] = initial_data['data_dir'] + 'Clean_data.csv' # name of merged dataframe
initial_data['clean_csv2'] = initial_data['data_dir'] + 'Clean_data_w_state.csv' # name of merged dataframe

# Define class methods and attributes
class Cities500(object):
    ''' 
    Class to handle data for 500 cities project
        +Will download data into pwd (or other specified dir)
        +Reads in variables from initial data dict
    '''
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
        self.mdf = pd.read_csv(self.merged_csv) # merged data with acs5 and 500c data

    def clean_data(self):
        '''
        drops unnamed rows (old indices) from dataframes so they can be merged
        '''
        for df in [self.mdf]:
            df.drop(columns = 'Unnamed: 0', inplace=True)

    def drop_pop_under_50(self):
        '''
        drop data with missing values
        '''
        self.clean = self.mdf[pd.isnull(self.mdf.Data_Value_Footnote_Symbol)] # drop data with pop <50 (b/c missing some data)
        cut_1 = len(self.clean)
        print(f'Dropped {len(self.mdf)-cut_1} for Pop. < 50')        
        self.clean = self.clean[pd.notnull(self.clean.Med_age)] # drop data with missing age 
        print(f'Dropped {cut_1-len(self.clean)} for missing age')        

    def create_results_df(self):
        '''Create a subset of cols in a new df. 
        Calculted variables will be passed to this df
        Outcome var from 500c data (Data_Value=% pop binge drinking)
        All predictors from acs5 2015 
        '''
        vois = ['Data_Value',
                'Med_age',
                'StateAbbr']
        self.df = self.clean[vois]

    def calc_vars_of_interest(self):        
        # self.df['M_F_total'] = self.clean['Male'] + self.clean['Female']
        self.df['Percent_female'] = self.clean['Female']/self.clean.Total_population

    def calc_education(self):
        edu_vars = [x for x in self.clean.columns if x.startswith('Education_25_')]
        edu_vars.remove('Education_25_1')
        self.clean['Education_25_total'] = self.clean[edu_vars].sum(axis=1) # matches Education_25_1
        less_than_hs_ged = ['Education_25_' + str(x) for x in range(2, 19)] # want _2:_18'B15003_018E' : 'Education_25_18', for hs diploma/GED
        self.df['Edu_less_than_hs_or_GED'] = (self.clean[less_than_hs_ged].sum(axis=1))/self.clean['Education_25_1']

    def calc_ipr(self):
        ipr_lt_1 = ['Income_to_poverty_ratio_' + str(x) for x in range(2, 6)] # want _2:_18'C17002_005E' for ipr < 1.5
        self.df['Income_to_pov_rat_lt_1.5'] = (self.clean[ipr_lt_1].sum(axis=1))/self.clean['Income_to_poverty_ratio_1']

    def calc_commute(self):
        commute_lt_30 = ['Commute_time_' + str(x) for x in range(2, 8)] # 'B08303_001E' : 'Commute_time_1', B08303_007E: Commute time under 30
        self.df['Commute_time_lt_30'] = (self.clean[commute_lt_30].sum(axis=1))/self.clean['Commute_time_1']
            
    def calc_work_depart(self):
        work_depart_8 = ['Work_depart_time_' + str(x) for x in range(2, 9)] # 'B08302_001E' : 'Work_depart_time_1',B08302_008E : before 8 am (include up to this)
        self.df['Work_depart_before_8am'] = (self.clean[work_depart_8].sum(axis=1))/self.clean['Work_depart_time_1']

    def calc_insurance(self):
        insurance_vars = [x for x in self.mdf.columns if x.startswith('Insurance')]
        insurance_vars = [x for x in insurance_vars if (x.endswith('_m_ins')) | (x.endswith('_f_ins'))]
        self.df['Percent_insured'] = (self.clean[insurance_vars].sum(axis=1))/self.clean['Insurance_total']

    def drop_missing(self):
        cut_1 = len(self.df)
        self.data = self.df.dropna()
        print(f'Dropped {cut_1-len(self.data)} for missing data')
        self.data.drop(columns='StateAbbr').to_csv(self.clean_csv, index=False)

    def dummy_code_state(self):
        self.data2 = pd.get_dummies(self.data)
        self.data2.drop(columns = 'StateAbbr_CO', inplace=True) # CO is reference state
        self.data2.to_csv(self.clean_csv2, index=False)

if __name__ == '__main__':
    cities = Cities500(initial_data)
    cities.load_data()
    cities.clean_data()
    cities.drop_pop_under_50()
    cities.create_results_df()
    cities.calc_vars_of_interest()
    cities.calc_education()
    cities.calc_ipr()
    cities.calc_commute()
    cities.calc_work_depart()
    cities.calc_insurance()
    cities.drop_missing()
    cities.dummy_code_state()