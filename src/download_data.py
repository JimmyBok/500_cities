# Import Packages
import os
import datetime
import requests
import pandas as pd 
import numpy as np 
'''
Dictionaries of variables to be pulled *requests must be > 50
Variables are stored as counts (except where noted)
So Total_population = population estimate, Male = estimated number of males, Female = estimated # of female
For larger categories, _1 denotes total and increasing variables denote increasing response (but not cumulative)
'''
edu_dict = {'NAME' :'Name', # dict of variables to pull and their corresponding names
            'B00001_001E' : 'Sample_count', # int val
            'B01003_001E' : 'Total_population', # int val
            'B01002_001E' : 'Med_age', # float val-not count
            'B01001_002E' : 'Male', # int
            'B01001_026E' : 'Female', #int
            'B15003_001E' : 'Education_25_1', # Educational attainment for 25+ total
            'B15003_002E' : 'Education_25_2', # no school
            'B15003_003E' : 'Education_25_3', # nursery 
            'B15003_004E' : 'Education_25_4', # kindergarten
            'B15003_005E' : 'Education_25_5', # 1st grade
            'B15003_006E' : 'Education_25_6', # 2nd grade
            'B15003_007E' : 'Education_25_7', # 3rd
            'B15003_008E' : 'Education_25_8', # 4th
            'B15003_009E' : 'Education_25_9', # 5th
            'B15003_010E' : 'Education_25_10', # 6th
            'B15003_011E' : 'Education_25_11', # 7th
            'B15003_012E' : 'Education_25_12', # 8th
            'B15003_013E' : 'Education_25_13', # 9th
            'B15003_014E' : 'Education_25_14', # 10th
            'B15003_015E' : 'Education_25_15', # 11th
            'B15003_016E' : 'Education_25_16', # 12th
            'B15003_017E' : 'Education_25_17', # HS diploma
            'B15003_018E' : 'Education_25_18', # GED or equiv
            'B15003_019E' : 'Education_25_19', # <1 yr college
            'B15003_020E' : 'Education_25_20', # some college, no degree
            'B15003_021E' : 'Education_25_21', # Associates degree
            'B15003_022E' : 'Education_25_22', # Bachelors degree
            'B15003_023E' : 'Education_25_23', # Masters degree
            'B15003_024E' : 'Education_25_24', # Professional school degree
            'B15003_025E' : 'Education_25_25'  # Doctorate degree
            }

income_dict = {'NAME' :'Name', 
            'C17002_001E' : 'Income_to_poverty_ratio_1', # Ratio of Income to Poverty (IPR) Level in the Past 12 Months
            'C17002_002E' : 'Income_to_poverty_ratio_2', # IPR <.50
            'C17002_003E' : 'Income_to_poverty_ratio_3', # .5 < IPR <.99
            'C17002_004E' : 'Income_to_poverty_ratio_4', # 1.00 < IPR <1.24
            'C17002_005E' : 'Income_to_poverty_ratio_5', # 1.25 < IPR <1.49
            'C17002_006E' : 'Income_to_poverty_ratio_6', # 1.50 < IPR <1.84
            'C17002_007E' : 'Income_to_poverty_ratio_7', # 1.85 < IPR <1.99
            'C17002_008E' : 'Income_to_poverty_ratio_8', # 2.00 < IPR
            'B08303_001E' : 'Commute_time_1', #B08303. Travel Time to Work 
            'B08303_002E' : 'Commute_time_2', # < 5mins
            'B08303_003E' : 'Commute_time_3', # 5-9 mins
            'B08303_004E' : 'Commute_time_4', # 10-14 mins
            'B08303_005E' : 'Commute_time_5', # 15-19 mins
            'B08303_006E' : 'Commute_time_6', # 20-24 mins
            'B08303_007E' : 'Commute_time_7', # 25-29 mins
            'B08303_008E' : 'Commute_time_8', # 30-34 mins
            'B08303_009E' : 'Commute_time_9', # 35-39 mins
            'B08303_010E' : 'Commute_time_10', # 40-44 mins
            'B08303_011E' : 'Commute_time_11', # 45-59 mins
            'B08303_012E' : 'Commute_time_12', # 60-89 mins
            'B08303_013E' : 'Commute_time_13', # 90+ mins
            'B08302_001E' : 'Work_depart_time_1', # B08302. Time Leaving Home to Go to Work 
            'B08302_002E' : 'Work_depart_time_2', # 00:00-4:59
            'B08302_003E' : 'Work_depart_time_3', # 05:00-5:29
            'B08302_004E' : 'Work_depart_time_4', # 05:30-5:59
            'B08302_005E' : 'Work_depart_time_5', # 06:00-6:29
            'B08302_006E' : 'Work_depart_time_6', # 06:30-6:59
            'B08302_007E' : 'Work_depart_time_7', # 07:00-7:29
            'B08302_008E' : 'Work_depart_time_8', # 07:30-7:59
            'B08302_009E' : 'Work_depart_time_9', # 08:00-8:29
            'B08302_010E' : 'Work_depart_time_10', # 08:30-8:59 
            'B08302_011E' : 'Work_depart_time_11', # 09:00-9:59
            'B08302_012E' : 'Work_depart_time_12', # 10:00-10:59
            'B08302_013E' : 'Work_depart_time_13', # 11:00-11:59
            'B08302_014E' : 'Work_depart_time_14', # 12:00-15:59
            'B08302_015E' : 'Work_depart_time_15' # 16:00-23:59
            }

ins_m_dict = {'NAME' :'Name', 
            'B27001_001E' : 'Insurance_total', # B27001. Health Insurance Coverage Status by Sex by Age
            'B27001_002E' : 'Insurance_males', # Total males
            'B27001_003E' : 'Insurance_lt_6_m_tot', # M, under 6 total
            'B27001_004E' : 'Insurance_lt_6_m_ins', # M, under 6 total ins
            'B27001_005E' : 'Insurance_lt_6_m_no_ins', # M, under 6 total not ins
            'B27001_006E' : 'Insurance_6_to_17_m_tot', # M, 6-17 total
            'B27001_007E' : 'Insurance_6_to_17_m_ins', # M, 6-17 total ins
            'B27001_008E' : 'Insurance_6_to_17_m_no_ins', # M, 6-17 total not ins
            'B27001_009E' : 'Insurance_18_to_24_m_tot', # M, 18-24 total 
            'B27001_010E' : 'Insurance_18_to_24_m_ins', # M, 18-24 total ins
            'B27001_011E' : 'Insurance_18_to_24_m_no_ins', # M, 18-24 total not ins
            'B27001_012E' : 'Insurance_25_to_34_m_tot', # M, 25-34 total  
            'B27001_013E' : 'Insurance_25_to_34_m_ins', # M, 25-34 total ins
            'B27001_014E' : 'Insurance_25_to_34_m_no_ins', # M, 25-34 total not ins
            'B27001_015E' : 'Insurance_35_to_44_m_tot', # M, 35-44 total
            'B27001_016E' : 'Insurance_35_to_44_m_ins', # M, 35-44 total ins
            'B27001_017E' : 'Insurance_35_to_44_m_no_ins', # M, 35-44 total not ins
            'B27001_018E' : 'Insurance_45_to_54_m_tot', # M, 45-54 total
            'B27001_019E' : 'Insurance_45_to_54_m_ins', # M, 45-54 total ins
            'B27001_020E' : 'Insurance_45_to_54_m_no_ins', # M, 45-54 total not ins
            'B27001_021E' : 'Insurance_55_to_64_m_tot', # M, 55-64 total 
            'B27001_022E' : 'Insurance_55_to_64_m_ins', # M, 55-64 total ins
            'B27001_023E' : 'Insurance_55_to_64_m_no_ins', # M, 55-64 total not ins
            'B27001_024E' : 'Insurance_65_to_74_m_tot', # M, 65-74 total 
            'B27001_025E' : 'Insurance_65_to_74_m_ins', # M, 65-74 total ins
            'B27001_026E' : 'Insurance_65_to_74_m_no_ins', # M, 65-74 total not ins
            'B27001_027E' : 'Insurance_gt_75_m_tot', # M, 75+ total
            'B27001_028E' : 'Insurance_gt_75_m_ins', # M, 75+ total ins
            'B27001_029E' : 'Insurance_gt_75_m_no_ins' # M, 75+ total not ins
            }

ins_f_dict = {'NAME' :'Name', # dict of variables to pull and their corresponding names
            'B27001_030E' : 'Insurance_females', # Total females
            'B27001_031E' : 'Insurance_lt_6_f_tot', # F, under 6 total
            'B27001_032E' : 'Insurance_lt_6_f_ins', # F, under 6 ins
            'B27001_033E' : 'Insurance_lt_6_f_no_ins', # F, under 6 not ins
            'B27001_034E' : 'Insurance_6_to_17_f_tot', # F, 6-17 total
            'B27001_035E' : 'Insurance_6_to_17_f_ins', # F, 6-17 ins 
            'B27001_036E' : 'Insurance_6_to_17_f_no_ins', # F, 6-17 not ins
            'B27001_037E' : 'Insurance_18_to_24_f_tot', # F, 18-24 tot
            'B27001_038E' : 'Insurance_18_to_24_f_ins', # F, 18-24 ins
            'B27001_039E' : 'Insurance_18_to_24_f_no_ins', # F, 18-24 not ins
            'B27001_040E' : 'Insurance_25_to_34_f_tot', # F, 25-34 tot
            'B27001_041E' : 'Insurance_25_to_34_f_ins', # F, 25-34 ins
            'B27001_042E' : 'Insurance_25_to_34_f_no_ins', # F, 25-34 not ins
            'B27001_043E' : 'Insurance_35_to_44_f_tot', # F, 35-44 total
            'B27001_044E' : 'Insurance_35_to_44_f_ins', # F, 35-44 ins
            'B27001_045E' : 'Insurance_35_to_44_f_no_ins', # F, 35-44 not ins
            'B27001_046E' : 'Insurance_45_to_54_f_tot', # F, 45-54 total
            'B27001_047E' : 'Insurance_45_to_54_f_ins', # F, 45-54 ins
            'B27001_048E' : 'Insurance_45_to_54_f_no_ins',  # F, 45-54 not ins
            'B27001_049E' : 'Insurance_55_to_64_f_tot', # F, 55-64 tot
            'B27001_050E' : 'Insurance_55_to_64_f_ins', # F, 55-64 ins 
            'B27001_051E' : 'Insurance_55_to_64_f_no_ins', # F, 55-64 not ins
            'B27001_052E' : 'Insurance_65_to_74_f_tot', # F, 65-74 tot
            'B27001_053E' : 'Insurance_65_to_74_f_ins', # F, 65-74 ins
            'B27001_054E' : 'Insurance_65_to_74_f_no_ins',  # F, 65-74 not ins
            'B27001_055E' : 'Insurance_gt_75_f_tot', # F, 75+ total
            'B27001_056E' : 'Insurance_gt_75_f_ins', # F, 75+ ins
            'B27001_057E' : 'Insurance_gt_75_f_no_ins' # F, 75+ not ins
            }

# pass dictionaries into intial dict for class access
vars_to_pull = [edu_dict, income_dict, ins_m_dict, ins_f_dict]

# Define class methods and attributes
class Cities500(object):
    ''' 
    Class to handle gathering data for 500 cities project
        +Will download data into pwd (or other specified dir)
        +Reads in variables from initial data dict
    '''
    def __init__(self, variables_to_pull, is_test=True):
        # Get pwd to set as home for project
        self.home = os.getcwd() + '/'
        self.time = datetime.datetime.now() # for timing download
        # home : '/home/danny/Desktop/galvanize/capstone1/' # Directory for all data and output (example of absolute path, otherwise use pwd)s
        self.key = os.environ['CENSUS_API_KEY'] # to pull acs5 data 
        self.url = 'https://data.cdc.gov/api/views/6vp6-wxuq/rows.csv?accessType=DOWNLOAD' # website 500 cities data is from
        self.is_test = True # By default only download test data (10 examples)
        # how to subset data-can be modified for city
        self.tract_subset = {
            'GeographicLevel' :'Census Tract', #select only tract level data
            'MeasureId' : 'BINGE', #select only binge drinking data
            'DataValueTypeID' : 'CrdPrv' #select only age-adjusted values
            }
        self.data_dir = self.home + '../data/' # Where output will be stored
        self.df_csv = self.data_dir + '500_Cities.csv' # name of 500c data
        self.sdf_csv = self.data_dir + 'Binge_Tract_Data.csv' # name of subset data 
        self.acs5_csv = self.data_dir + 'ACS5_data.csv' # name of downloaded tract data
        self.merged_csv = self.data_dir + 'Merged_data.csv' # name of merged dataframe
        self.dicts_to_pull = variables_to_pull

    def run_download(self):
        # check for data directory, if not there (and therefore data not there) make dir
        self.create_dirs()
        self.get_500c_data()
        self.subset_500c_data()
        self.acs5_request()

    def create_dirs(self):
        '''
        Creates directories for 500 cities analysis
            +data dir to store data files (csvs)
        '''
        for mydir in [self.data_dir]:
            self.make_dirs(mydir)

    def make_dirs(self, dirpath):
        if not os.path.isdir(dirpath):
            print(f'Creating directory: {dirpath}')
            os.makedirs(dirpath, exist_ok=True)
        else:
            print(f"Directory exists: {dirpath}")

    def get_500c_data(self):
        '''
        Gets data for 500 cities analysis
            looks for file self.df_csv, if not there attempts to download data
            from self.url
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
            For key, value in self.tract_subset,
            cuts self.df using self.df[self.df[key]==value]
        RETURNS
        -------
        self.sdf: pd dataframe
            subset data with only rows of interest
            resets index for easier merging with later generated results
        '''
        if os.path.isfile(self.sdf_csv):
            self.sdf = pd.read_csv(self.sdf_csv)
            print(f'Subset data exists, using: {self.sdf_csv}')
        else:
            for key, value in self.tract_subset.items():
                if not hasattr(self, 'sdf'): # if subset data does NOT exist
                    self.sdf = self.df[self.df[key] == value]
                else: # if subset data has already been created
                    self.sdf = self.sdf[self.sdf[key] == value]
            self.sdf.reset_index(inplace=True, drop=True) # reset index for merging later
            self.sdf.to_csv(self.sdf_csv) # write out subset data for inspection
            print(f'Subset df written to: {self.sdf_csv}')
            print(f'Shape of subset df is {self.sdf.shape}')
            self.parse_tract() # creates str variables for state, county, tract from TractFIPS
 

    def parse_tract(self):
        self.sdf['Tract_str'] = self.sdf['TractFIPS'].apply(lambda x: '%011.0f' %x) 
        self.sdf['state']= self.sdf['Tract_str'].apply(lambda x: x[:2])
        self.sdf['county']= self.sdf['Tract_str'].apply(lambda x: x[2:5])
        self.sdf['tract']= self.sdf['Tract_str'].apply(lambda x: x[5:])

    def acs5_request(self):
        if not self.does_data_exists():
            if self.is_test: # if is test, select only first few rows
                    self.mdf = self.sdf.iloc[:10] 
            else: # run on whole df, can take hours (~15)
                self.mdf = self.sdf
            num_runs = len(self.dicts_to_pull)
            max_id = len(self.mdf) # to help know how much more to go
            print(f'Downloading data from ACS5. This may take upwards of 15 hours and requires a valid API key')
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
                    temp = self.pull_request(index, row, var_names_req)
                    self.results = self.results.append(temp, ignore_index=True)
                self.acs5 = self.results.rename(index=str, columns=my_dict) # rename columns with meaningful names
                self.acs5.reset_index(inplace=True, drop=True) # reset index for merging later
                self.acs5.to_csv(self.acs5_csv) 
                cols_to_use = self.acs5.columns.difference(self.mdf.columns) # avoid repetitive columns 
                self.mdf = pd.merge(self.mdf, self.acs5[cols_to_use], left_index=True, right_index=True, how='outer')
                self.mdf.to_csv(self.merged_csv)
                cnt +=1 

    def does_data_exists(self):
        if os.path.isfile(self.merged_csv):
            print(f"Data file {self.merged_csv} exists, not downloading new data")
            return True
        if os.path.isfile(self.acs5_csv):
            print(f"ACS5_data exists, attempting to merged {self.acs5_csv}")
            cols_to_use = self.acs5.columns.difference(self.mdf.columns) # avoid repetitive columns 
            self.mdf = pd.merge(self.mdf, self.acs5[cols_to_use], left_index=True, right_index=True, how='outer')
            self.mdf.to_csv(self.merged_csv)
            return True
        return False

    def pull_request(self, index, row, var_names_req):
        ret = pd.Series() # empty series to pass data to
        self.req = f'https://api.census.gov/data/2015/acs5?get={var_names_req}&for=tract:{row.tract}&in=state:{row.state}in=county:{row.county}&key={self.key}'
        self.r = requests.get(self.req)
        print(self.r.status_code)
        if self.r.status_code == 200: # pass row when request gets errors
            self.temp = pd.DataFrame(self.r.json())  
            self.temp = self.temp.rename(columns=self.temp.iloc[0]).drop(self.temp.index[0])
            self.temp['index_val'] = index
        else: # pass empty dataframe to join to help keep indices aligned 
            self.temp = pd.DataFrame()
            self.temp = self.temp.append({'index_val': index}, ignore_index=True)
        return self.temp

if __name__ =='__main__':
    cities = Cities500(vars_to_pull, is_test=True)
    cities.run_download()