import numpy as np
from scipy.stats import mannwhitneyu
from scipy.stats import ks_2samp
from scipy.stats import kstest
from scipy.stats import shapiro
from scipy.stats import anderson
from statsmodels.stats.diagnostic import lilliefors
import os
import pandas as pd

def mannwhitneyu_test(data_1 : np.array, data_2 : np.array):
    """two sided mann whitney u test. returns stat, p"""
    return mannwhitneyu(data_1, data_2, alternative ='two-sided')

def read_df_from_folder(folder):
    """reads all the csv in the folder into a list of dataframes. returns list of dataframes"""
    return [pd.read_csv(os.path.join(folder, filename)) for filename in os.listdir(folder)]

def read_col_from_dataframes(df_list, col_name):
    """reads a certain column (f.e. 'dist') from all the dataframes in the df_list and returns them as a list of numpy arrays"""
    return [df_list[j][col_name].to_numpy() for j in range(0, len(df_list))]

def read_cols_from_folder(folder, col_name):
    """reads a certain column from all the csv in the folder and returns them as a list of arrays"""
    df_list = read_df_from_folder(folder)
    columns = read_col_from_dataframes(df_list, col_name)
    return columns

def hypothesis_test(data_1 : np.array, data_2 : np.array, test_name):
    mwu_names = ['mannwhitneyu', 'mwu', 'mw', 'mannwhitney', 'mannwhitney_u', 'MWU', 'MW', 'MannWhitneyU', 'MannWhitney', 'MannWhitney_u']
    ks_names = ['ks', 'ks2', 'ks_2', 'ks_2samp', 'ks2samp', 'KS', 'KS2', 'KS_2', 'KS_2samp', 'KS2samp']
    if test_name in mwu_names:
        return mannwhitneyu_test(data_1, data_2)
    elif test_name in ks_names:
        return ks_2samp(data_1, data_2)
    else:
        raise ValueError('invalid test name')
    
def hypothesis_test_list(data_list_1 : list, data_list_2 : list, test_name):
    """hypothesis test on the numpy arrays in the two given lists (pairwise with same index). returns list of [stat, p] in each entry"""
    return [hypothesis_test(data_list_1[i], data_list_2[i], test_name).pvalue for i in range(0, len(data_list_1))]
    
def folder_names_from_folder_paths(folders):
    """derives column names from the folder names."""
    return [name.split('/')[-1].split('_',1)[1].replace('_','\_') for name in folders]