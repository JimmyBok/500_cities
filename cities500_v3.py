'''
Script to analyze 500 Cities data obtained from 
https://catalog.data.gov/dataset/500-cities-local-data-for-better-health-b32fd

Completed as part of Galvanize Data Science Immersive Capstone 1

Written by Danny Lumian, 2018
'''
# Import Packages
import os
import sys
import requests
import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt 
from scipy import stats
from uszipcode import SearchEngine
# Get pwd to set as home for project
home = os.getcwd() + '/'
#Set up variables in dict to pass to class
initial_data = {
    'url' :'https://data.cdc.gov/api/views/6vp6-wxuq/rows.csv?accessType=DOWNLOAD', # website 500 cities data is from
    'home' : home, # Directory for all data and output using pwd
#   'home' : '/home/danny/Desktop/galvanize/capstone1/' # Directory for all data and output (example of absolute path, otherwise use pwd)s
    'data_subset' : {
        'GeographicLevel' :'City', #select only city level data
        'MeasureId' : 'BINGE', #select only binge drinking data
        'DataValueTypeID' : 'AgeAdjPrv' #select only age-adjusted values
    }
}
# Additonal variables that have to be added once the dict is input
#   Due to referencing other objects in the dict
initial_data['data_dir'] = initial_data['home'] + 'data/'
initial_data['img_dir'] = initial_data['home'] + 'images/'
initial_data['df_csv'] = initial_data['data_dir'] + '500_Cities_2017.csv'
initial_data['sdf_csv'] = initial_data['data_dir'] + 'Binge_City_Data.csv'
initial_data['med_income_csv'] = initial_data['data_dir'] + 'Med_income.csv'

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
        for mydir in [self.img_dir, self.data_dir]:
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
        if not os.path.isfile(self.df_csv):
            print('Missing data, attempting to download...')
            print('This may take a few minutes...')
            response = requests.get(self.url)
            with open(self.df_csv, 'wb') as f:
                f.write(response.content)
        else:
            print(f'Data exists. Using file {self.df_csv}')

    def load_500c_data(self):
        '''
        loads data for 500 cities analysis from self.df_csv into pandas df
        PARAMETERS
        ----------
        None

        RETURNS
        -------
        None
        '''
        self.df = pd.read_csv(self.df_csv)
        print(f'Shape of 500 cities df is {self.df.shape}')
        print(f'Columns of 500 cities df are {self.df.columns}')

    def subset_500c_data(self):
        '''
        Gets subset data for 500 cities analysis
            For key, value in self.data_subset,
            cuts self.df using self.df[self.df[key]==value]
        PARAMETERS
        ----------
        None

        RETURNS
        -------
        self.sdf: pd dataframe
            subset data with only rows of interest
            resets index for easier merging with later generated results
        '''
        for key, value in self.data_subset.items():
            if not hasattr(self, 'sdf'):
                self.sdf = self.df[self.df[key] == value]
            else:
                self.sdf = self.sdf[self.sdf[key] == value]
        self.sdf.reset_index(inplace=True)
        self.sdf.to_csv(self.sdf_csv)
        print(f'Subset df written to: {self.sdf_csv}')
        print(f'Shape of subset df is {self.sdf.shape}')

    def get_med_income(self):
        '''
        generates median incomde data based on city, state for each row
        uses uszipcode data
        generates a query for each row in self.sdf
        PARAMETERS
        ----------
        None

        RETURNS
        -------
        self.results: pd dataframe
            contains median income, count of matching zip codes and number of zips with med income data
        '''
        print('Generating median incomes from uszipcode...')
        print('This may take a few minutes...')
        self.results = pd.DataFrame()
        search = SearchEngine(simple_zipcode=True)
        for index, row in self.sdf.iterrows():
            ret = pd.Series()
            med_incomes = []
            res = search.by_city_and_state(row.CityName, row.StateAbbr, returns=100)
            ret['Zip_cnt'] = len(res)
            usable_incomes = 0
            for i in res:
                if i.median_household_income:
                    usable_incomes += 1
                    med_incomes.append(i.median_household_income)
            ret['Zip_w_income']= usable_incomes
            ret['med_income'] = np.mean(med_incomes)
            self.results=self.results.append(ret, ignore_index=True)
        cities.mdf = cities.sdf.join(cities.results)
        cities.mdf.to_csv(self.med_income_csv)

if __name__ =='__main__':
    cities = Cities500(initial_data)
    cities.create_dirs()
    if not os.path.isfile(cities.df_csv):
        cities.get_500c_data()
    cities.load_500c_data()
    cities.subset_500c_data()
    if not os.path.isfile(cities.med_income_csv):
        cities.get_med_income()
    else:
        print(f"Data detected. Loading from {cities.med_income_csv}")
        cities.mdf = pd.read_csv(cities.med_income_csv)


