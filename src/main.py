from download_data import vars_to_pull
from clean_data import CleanData

if __name__ =='__main__':
    data_cleaner = CleanData(vars_to_pull, is_test=True)
    data_cleaner.run_download()
    data_cleaner.clean_data()