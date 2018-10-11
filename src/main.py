from download_data import vars_to_pull
from clean_data import CleanData
from analyze_data import Results, initial_data
from analyze_data_sklearn import SkLearnResults, init_data
from linear_regression_analysis import LinearData
if __name__ =='__main__':
    data_cleaner = CleanData(vars_to_pull, is_test=True)
    # Note: downloading all data can take 12+ hours
    #   Will skip if data exists (if partial download occured must move files for fresh download)
    data_cleaner.run_download()
    data_cleaner.clean_data()
    # Calculating residuals can take 30+ minutes
    results = Results(initial_data)
    results.run_analyze()
    sklresults = SkLearnResults(init_data)
    sklresults.run_sk_analysis()
    lrd = LinearData(init_data)
    lrd.run_linear_analysis()
