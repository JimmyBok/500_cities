# Import Packages
import os
import datetime
import requests
import concurrent.futures
import pandas as pd 
import numpy as np 
# Get pwd to set as home for project
home = os.getcwd() + '/'
my_key = os.environ['CENSUS_API_KEY'] # to pull acs5 data 
time = datetime.datetime.now() # Write outputs with date/time to avoid overwriting outputs
date_str = time.strftime("%Y_%m_%d")
#Set up variables in dict to pass to class
initial_data = {
    'url' :'https://data.cdc.gov/api/views/6vp6-wxuq/rows.csv?accessType=DOWNLOAD', # website 500 cities data is from
    'home' : home, # Directory for all data and output using pwd
#   'home' : '/home/danny/Desktop/galvanize/capstone1/' # Directory for all data and output (example of absolute path, otherwise use pwd)s
    'date_str' : date_str,
    'time' : time, # to clock downloading times
    # 'results' : pd.DataFrame(), # results dataframe for aggregation
    'tract_subset' : {
        'GeographicLevel' :'Census Tract', #select only tract level data
        'MeasureId' : 'BINGE', #select only binge drinking data
        'DataValueTypeID' : 'CrdPrv' #select only age-adjusted values
    }
}
# Additonal variables that have to be added once the dict is input
#   Due to referencing other objects in the dict
initial_data['data_dir'] = initial_data['home'] + 'data/' # Where output will be stored
initial_data['df_csv'] = initial_data['data_dir'] + '500_Cities_2017.csv' # name of 500c data
initial_data['sdf_csv'] = initial_data['data_dir'] + 'Binge_Tract_Data.csv' # name of subset data 
initial_data['acs5_csv'] = initial_data['data_dir'] + 'ACS5_data_' + date_str + '.csv' # name of downloaded tract data
initial_data['merged_csv'] = initial_data['data_dir'] + 'Merged_data_' + date_str + '.csv' # name of merged dataframe
# Dictionaries of variables to be pulled *requests must be < 50
# Can't be initialized in self b/c has to be referenced in method arg
edu_dict = {'NAME' :'Name', # dict of variables to pull and their corresponding names
            'B00001_001E' : 'Sample_count', # int val
            'B01003_001E' : 'Total_population', # int val
            'UR'          : 'Urban_rural', # Urban or rural
            'B01002_001E' : 'Med_age', # flt
            'B01001_002E' : 'Male', # int
            'B01001_026E' : 'Female', #int
            'B15003_001E' : 'Education_25_1', # TOTAL
            'B15003_002E' : 'Education_25_2', # TOTAL
            'B15003_003E' : 'Education_25_3', # TOTAL
            'B15003_004E' : 'Education_25_4', # TOTAL
            'B15003_005E' : 'Education_25_5', # TOTAL
            'B15003_006E' : 'Education_25_6', # TOTAL
            'B15003_007E' : 'Education_25_7', # TOTAL
            'B15003_008E' : 'Education_25_8', # TOTAL
            'B15003_009E' : 'Education_25_9', # TOTAL
            'B15003_010E' : 'Education_25_10', # TOTAL
            'B15003_011E' : 'Education_25_11', # TOTAL
            'B15003_012E' : 'Education_25_12', # TOTAL
            'B15003_013E' : 'Education_25_13', # TOTAL
            'B15003_014E' : 'Education_25_14', # TOTAL
            'B15003_015E' : 'Education_25_15', # TOTAL
            'B15003_016E' : 'Education_25_16', # TOTAL
            'B15003_017E' : 'Education_25_17', # TOTAL
            'B15003_018E' : 'Education_25_18', # TOTAL
            'B15003_019E' : 'Education_25_19', # TOTAL
            'B15003_020E' : 'Education_25_20', # TOTAL
            'B15003_021E' : 'Education_25_21', # TOTAL
            'B15003_022E' : 'Education_25_22', # TOTAL
            'B15003_023E' : 'Education_25_23', # TOTAL
            'B15003_024E' : 'Education_25_24', # TOTAL
            'B15003_025E' : 'Education_25_25'
            }

income_dict = {'NAME' :'Name', # dict of variables to pull and their corresponding names
            'C17002_001E' : 'Income_to_poverty_ratio_1',
            'C17002_002E' : 'Income_to_poverty_ratio_2',
            'C17002_003E' : 'Income_to_poverty_ratio_3',
            'C17002_004E' : 'Income_to_poverty_ratio_4',
            'C17002_005E' : 'Income_to_poverty_ratio_5',
            'C17002_006E' : 'Income_to_poverty_ratio_6',
            'C17002_007E' : 'Income_to_poverty_ratio_7',
            'C17002_008E' : 'Income_to_poverty_ratio_8',
            'B08303_001E' : 'Commute_time_1',
            'B08303_002E' : 'Commute_time_2',
            'B08303_003E' : 'Commute_time_3',
            'B08303_004E' : 'Commute_time_4',
            'B08303_005E' : 'Commute_time_5',
            'B08303_006E' : 'Commute_time_6',
            'B08303_007E' : 'Commute_time_7',
            'B08303_008E' : 'Commute_time_8',
            'B08303_009E' : 'Commute_time_9',
            'B08303_010E' : 'Commute_time_10',
            'B08303_011E' : 'Commute_time_11',
            'B08303_012E' : 'Commute_time_12',
            'B08303_013E' : 'Commute_time_13',
            'B08302_001E' : 'Work_depart_time_1',
            'B08302_002E' : 'Work_depart_time_2',
            'B08302_003E' : 'Work_depart_time_3',
            'B08302_004E' : 'Work_depart_time_4',
            'B08302_005E' : 'Work_depart_time_5',
            'B08302_006E' : 'Work_depart_time_6',
            'B08302_007E' : 'Work_depart_time_7',
            'B08302_008E' : 'Work_depart_time_8',
            'B08302_009E' : 'Work_depart_time_9',
            'B08302_010E' : 'Work_depart_time_10',
            'B08302_011E' : 'Work_depart_time_11',
            'B08302_012E' : 'Work_depart_time_12',
            'B08302_013E' : 'Work_depart_time_13',
            'B08302_014E' : 'Work_depart_time_14',
            'B08302_015E' : 'Work_depart_time_15'
            }

ins_m_dict = {'NAME' :'Name', # dict of variables to pull and their corresponding names
            'B27001_001E' : 'Insurance_total',
            'B27001_002E' : 'Insurance_males',
            'B27001_003E' : 'Insurance_lt_6_m_tot',
            'B27001_004E' : 'Insurance_lt_6_m_ins',
            'B27001_005E' : 'Insurance_lt_6_m_no_ins',
            'B27001_006E' : 'Insurance_6_to_17_m_tot',
            'B27001_007E' : 'Insurance_6_to_17_m_ins',
            'B27001_008E' : 'Insurance_6_to_17_m_no_ins',
            'B27001_009E' : 'Insurance_18_to_24_m_tot',
            'B27001_010E' : 'Insurance_18_to_24_m_ins',
            'B27001_011E' : 'Insurance_18_to_24_m_no_ins',
            'B27001_012E' : 'Insurance_25_to_34_m_tot',
            'B27001_013E' : 'Insurance_25_to_34_m_ins',
            'B27001_014E' : 'Insurance_25_to_34_m_no_ins',
            'B27001_015E' : 'Insurance_35_to_44_m_tot',
            'B27001_016E' : 'Insurance_35_to_44_m_ins',
            'B27001_017E' : 'Insurance_35_to_44_m_no_ins',
            'B27001_018E' : 'Insurance_45_to_54_m_tot',
            'B27001_019E' : 'Insurance_45_to_54_m_ins',
            'B27001_020E' : 'Insurance_45_to_54_m_no_ins',
            'B27001_021E' : 'Insurance_55_to_64_m_tot',
            'B27001_022E' : 'Insurance_55_to_64_m_ins',
            'B27001_023E' : 'Insurance_55_to_64_m_no_ins',
            'B27001_024E' : 'Insurance_65_to_74_m_tot',
            'B27001_025E' : 'Insurance_65_to_74_m_ins',
            'B27001_026E' : 'Insurance_65_to_74_m_no_ins',
            'B27001_027E' : 'Insurance_gt_75_m_tot',
            'B27001_028E' : 'Insurance_gt_75_m_ins',
            'B27001_029E' : 'Insurance_gt_75_m_no_ins'
            }
ins_f_dict = {'NAME' :'Name', # dict of variables to pull and their corresponding names
            'B27001_030E' : 'Insurance_females',
            'B27001_031E' : 'Insurance_lt_6_f_tot',
            'B27001_032E' : 'Insurance_lt_6_f_ins',
            'B27001_033E' : 'Insurance_lt_6_f_no_ins',
            'B27001_034E' : 'Insurance_6_to_17_f_tot',
            'B27001_035E' : 'Insurance_6_to_17_f_ins',
            'B27001_036E' : 'Insurance_6_to_17_f_no_ins',
            'B27001_037E' : 'Insurance_18_to_24_f_tot',
            'B27001_038E' : 'Insurance_18_to_24_f_ins',
            'B27001_039E' : 'Insurance_18_to_24_f_no_ins',
            'B27001_040E' : 'Insurance_25_to_34_f_tot',
            'B27001_041E' : 'Insurance_25_to_34_f_ins',
            'B27001_042E' : 'Insurance_25_to_34_f_no_ins',
            'B27001_043E' : 'Insurance_35_to_44_f_tot',
            'B27001_044E' : 'Insurance_35_to_44_f_ins',
            'B27001_045E' : 'Insurance_35_to_44_f_no_ins',
            'B27001_046E' : 'Insurance_45_to_54_f_tot',
            'B27001_047E' : 'Insurance_45_to_54_f_ins',
            'B27001_048E' : 'Insurance_45_to_54_f_no_ins',
            'B27001_049E' : 'Insurance_55_to_64_f_tot',
            'B27001_050E' : 'Insurance_55_to_64_f_ins',
            'B27001_051E' : 'Insurance_55_to_64_f_no_ins',
            'B27001_052E' : 'Insurance_65_to_74_f_tot',
            'B27001_053E' : 'Insurance_65_to_74_f_ins',
            'B27001_054E' : 'Insurance_65_to_74_f_no_ins',
            'B27001_055E' : 'Insurance_gt_75_f_tot',
            'B27001_056E' : 'Insurance_gt_75_f_ins',
            'B27001_057E' : 'Insurance_gt_75_f_no_ins'
            }

# dicts_to_pull = [edu_dict, income_dict, ins_m_dict, ins_f_dict]
initial_data['dicts_to_pull'] = [edu_dict, income_dict, ins_m_dict, ins_f_dict]
# initial_data['dicts_to_pull'] = [edu_dict]

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

    def make_dirs(self, dirpath):
        '''
        Creates directory (dirpath)
        PARAMETERS
        ----------
        dirpath : str
            file path to be created, will pass if already exists
        RETURNS
        -------
        None
        '''
        if not os.path.isdir(dirpath):
            print(f'Creating directory: {dirpath}')
            os.makedirs(dirpath, exist_ok=True)
        else:
            print(f"Directory exists: {dirpath}")

    def create_dirs(self):
        '''
        Creates directories for 500 cities analysis
            +data dir to store data files (csvs)
            +images dir to store image files (pngs)
        PARAMETERS
        ----------
        None

        RETURNS
        -------
        None
        '''
        for mydir in [self.data_dir]:
            self.make_dirs(mydir)

    def get_500c_data(self):
        '''
        Gets data for 500 cities analysis
            looks for file self.df_csv, if not there attempts to download data
            from self.url
        PARAMETERS
        ----------
        None

        RETURNS
        -------
        None
        '''
        if not os.path.isfile(self.df_csv): # if no csv file is found
            print('Missing data, attempting to download...')
            print('This may take a few minutes...')
            response = requests.get(self.url)
            with open(self.df_csv, 'wb') as f:
                f.write(response.content)
        else: # if data already exists
            print(f'Data exists. Using file {self.df_csv}')
        self.df = pd.read_csv(self.df_csv) # load data into self.df
        print(f'Shape of 500 cities df is {self.df.shape}')
        print(f'Columns of 500 cities df are {self.df.columns}')

    def subset_500c_data(self):
        '''
        Gets subset data for 500 cities analysis
            For key, value in my_dict,
            cuts self.df using self.df[self.df[key]==value]
        PARAMETERS
        ----------
        RETURNS
        -------
        self.sdf: pd dataframe
            subset data with only rows of interest
            resets index for easier merging with later generated results
        '''
        for key, value in self.tract_subset.items():
            if not hasattr(self, 'sdf'): # if subset data does NOT exist
                self.sdf = self.df[self.df[key] == value]
            else: # if subset data has already been created
                self.sdf = self.sdf[self.sdf[key] == value]
        self.sdf.reset_index(inplace=True, drop=True) # reset index for merging later
        self.sdf.to_csv(self.sdf_csv) # write out subset data for inspection
        print(f'Subset df written to: {self.sdf_csv}')
        print(f'Shape of subset df is {self.sdf.shape}')

    def parse_tract(self):
        self.sdf['Tract_str'] = self.sdf['TractFIPS'].apply(lambda x: '%011.0f' %x) 
        self.sdf['state']= self.sdf['Tract_str'].apply(lambda x: x[:2])
        self.sdf['county']= self.sdf['Tract_str'].apply(lambda x: x[2:5])
        self.sdf['tract']= self.sdf['Tract_str'].apply(lambda x: x[5:])

    def acs5_request(self, run_test=True):
        if not hasattr(self, 'mdf'): # if merge data does NOT exist
            if run_test: # if run_test is true only use first 10 rows of data
                self.mdf = self.sdf.iloc[:10] 
            else:
                self.mdf = self.sdf
        num_runs = len(self.dicts_to_pull)
        max_id = len(self.mdf) # to help know how much more to go
        print(f'Downloading data from ACS5. This may take hours and requires a valid API key')
        cnt = 1
        for my_dict in self.dicts_to_pull:
            self.results = pd.DataFrame()
            var_list = list(my_dict.keys())
            var_names_req = (',').join(var_list)  # list of variable ids to pass to request
            for index, row in self.mdf.iterrows():
                print(f'Pulling dictionary {str(cnt)} of {str(num_runs)}')
                print(f'At index {index} of {max_id}.\n{index/max_id*100} percent done.')
                time_delta = datetime.datetime.now() - self.time
                print(f'Elapsed minutes: {time_delta.total_seconds()/60}')
                ret = pd.Series() # empty series to pass data to
                self.req = f'https://api.census.gov/data/2015/acs5?get={var_names_req}&for=tract:{row.tract}&in=state:{row.state}in=county:{row.county}&key={my_key}'
                self.r = requests.get(self.req)
                print(self.r.status_code)
                if self.r.status_code == 200: # pass row when request gets errors
                    self.temp = pd.DataFrame(self.r.json())  
                    self.temp = self.temp.rename(columns=self.temp.iloc[0]).drop(self.temp.index[0])
                    self.temp['index_val'] = index
                else: # pass empty dataframe to join to help keep indices aligned 
                    self.temp = pd.DataFrame()
                    self.temp = self.temp.append({'index_val': index}, ignore_index=True)
                self.results = self.results.append(self.temp, ignore_index=True)
            self.acs5 = self.results.rename(index=str, columns=my_dict) # rename columns with meaningful names
            self.acs5.reset_index(inplace=True, drop=True) # reset index for merging later
            self.acs5.to_csv(self.acs5_csv) 
            cols_to_use = self.acs5.columns.difference(self.mdf.columns) 
            self.mdf = pd.merge(self.mdf, self.acs5[cols_to_use], left_index=True, right_index=True, how='outer')
            self.mdf.to_csv(self.merged_csv)
            cnt +=1 

if __name__ =='__main__':
    cities = Cities500(initial_data)
    cities.create_dirs()
    cities.get_500c_data()
    cities.subset_500c_data()
    cities.parse_tract()
    cities.acs5_request(run_test=False)