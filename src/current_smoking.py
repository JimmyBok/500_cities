import os
import pandas as pd
from download_data import vars_to_pull
from clean_data import CleanData
from analyze_data import Results, initial_data
from analyze_data_sklearn import SkLearnResults, init_data
from linear_regression_analysis import LinearData

class CurrentSmoking(CleanData):

    def __init__(self, *args, **kwargs):
        super(CurrentSmoking,self).__init__(*args, **kwargs)
        self.clean_csv = self.data_dir + 'Smoking_clean_data.csv' # name of merged dataframe
        self.clean_csv_w_states = self.data_dir + 'Smoking_clean_data_w_state.csv' # name of merged dataframe
        self.sdf_csv = self.data_dir + 'Smoking_Tract_Data.csv'
        self.tract_subset = {
            'GeographicLevel' :'Census Tract', #select only tract level data
            'MeasureId' : 'CSMOKING', #select only binge drinking data
            'DataValueTypeID' : 'CrdPrv' #select only age-adjusted values
            }

    def clean_data(self):
        self.load_data()
        self.subset_500c_data()
        self.replace_data_value()
        self.drop_unnamed_cols()
        self.drop_pop_under_50()
        self.create_results_df()
        self.calc_vars_of_interest()
        self.calc_education()
        self.calc_ipr()
        self.calc_commute()
        self.calc_work_depart()
        self.calc_insurance()
        self.drop_missing()
        self.dummy_code_state()

    def replace_data_value(self):
        '''
        Updates target values from binge drinking to smoking 
        Uses same variable name (Data_Value) so can be run in other scripts without issue
        '''
        print(f'Mean of old data value is{self.mdf.Data_Value.mean()}')
        self.mdf['Data_Value']=self.sdf['Data_Value']
        print(f'Mean of new data value is{self.mdf.Data_Value.mean()}')


if __name__ =='__main__':
    data_cleaner = CurrentSmoking(vars_to_pull, is_test=True)
    # Note: downloading all data can take 12+ hours
    #   Will skip if data exists (if partial download occured must move files for fresh download)
    data_cleaner.run_download()
    data_cleaner.clean_data()

    # Get pwd to set as home for project
    home = os.getcwd() + '/' # where we are,
    img_dir = home + '../images_smoking/' # where images live
    data_dir = home + '../data/' # where data live
    merged_csv = data_dir + 'Merged_data.csv' # original data by tract (to get N)
    clean_csv = data_dir + 'Smoking_clean_data_w_state.csv' # cleaned data to analyze
    #create dict to pass variables names to class

    initial_data = { 'home' : home,
                    'img_dir' : img_dir, 
                    'data_dir' : data_dir,
                    'merged_csv' : merged_csv,
                    'clean_csv' : clean_csv,
                    'cv' : 10, 
                    'random_seed': 42,
                    'score_type': 'neg_mean_squared_error',
                    'results' : pd.DataFrame()
                    }
    initial_data['df_csvs'] = {'orig' : initial_data['merged_csv'],
                                'data': initial_data['clean_csv']
                            }


    results = Results(initial_data)
    results.run_analyze()
    sklresults = SkLearnResults(initial_data)
    sklresults.run_sk_analysis()
    lrd = LinearData(initial_data)
    lrd.load_data()
    lrd.get_target_predictors()
    lrd.split_data()
    lrd.linear_regression()
    lrd.create_df_w_name_coef()
    lrd.create_table_of_demos()
    lrd.plot_state_coeffs(title='Impact of State on Smoking')