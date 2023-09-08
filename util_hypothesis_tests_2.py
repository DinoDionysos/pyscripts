import numpy as np
from scipy.stats import mannwhitneyu
from scipy.stats import ks_2samp
from scipy.stats import kstest
from scipy.stats import shapiro
from scipy.stats import anderson
from statsmodels.stats.diagnostic import lilliefors
from scipy.stats import brunnermunzel
from scipy.stats import levene
from scipy.stats import kruskal
from scipy.stats import normaltest
from scipy.stats import spearmanr
from scipy.stats import kendalltau
import os
import pandas as pd

def kendallstau(data_1 : np.array, data_2 : np.array):
    """kendall's tau. returns stat, p"""
    return kendalltau(data_1, data_2, alternative='less')

def spearmanr(data_1 : np.array, data_2 : np.array):
    """spearman's r. returns stat, p"""
    return spearmanr(data_1, data_2)

def kruskalwallis_test(data_1 : np.array, data_2 : np.array):
    """kruskal test. returns stat, p"""
    return kruskal(data_1, data_2, nan_policy='omit')

def brunnermunzel_test(data_1 : np.array, data_2 : np.array):
    """two sided brunner munzel test. returns stat, p"""
    return brunnermunzel(data_1, data_2, alternative='two-sided')

def brownforsythe_test(data_1 : np.array, data_2 : np.array):
    """two sided brown forsythe test. returns stat, p"""
    return levene(data_1, data_2, center='median')

def mannwhitneyu_test(data_1 : np.array, data_2 : np.array):
    """two sided mann whitney u test. returns stat, p"""
    return mannwhitneyu(data_1, data_2, alternative ='two-sided')

def levene_f(data_1 : np.array, data_2 : np.array):
    """computes the f value for the levene test"""
    return np.var(data_1)/np.var(data_2)

def f_value_mwu(data_1 : np.array, data_2 : np.array):
    """computes the f value for the mann whitney u test"""
    U, _ = mannwhitneyu_test(data_1, data_2)
    return U/len(data_1)/len(data_2)

def r_values_mwu(data_1 : np.array, data_2 : np.array):
    """computes the r values for the mann whitney u test"""
    f_1 = f_value_mwu(data_1, data_2)
    f_2 = f_value_mwu(data_2, data_1)
    return f_1 - f_2

def shapiro_test(data : np.array):
    """shapiro test. returns stat, p"""
    return shapiro(data)

def anderson_test(data : np.array):
    """anderson test. returns stat, critical values, significance levels"""
    return anderson(data)

def ks_norm_test(data : np.array):
    """ks test. returns stat, p"""
    return kstest(data, 'norm')

def skew_kurtosis_test(data : np.array):
    """skew kurtosis test. returns stat, p"""
    return normaltest(data)

def lilliefors_test(data : np.array):
    """lilliefors test. returns stat, p"""
    return lilliefors(data)

def read_df_from_folder(folder):
    """reads all the csv in the folder into a list of dataframes. returns list of dataframes"""
    sorted_folders = sorted(os.listdir(folder))
    return [pd.read_csv(os.path.join(folder, filename)) for filename in sorted_folders]

def read_col_from_dataframes(df_list, col_name):
    """reads a certain column (f.e. 'dist') from all the dataframes in the df_list and returns them as a list of numpy arrays"""
    return [df_list[j][col_name].to_numpy() for j in range(0, len(df_list))]

def read_cols_from_folder(folder, col_name):
    """reads a certain column from all the csv in the folder and returns them as a list of arrays"""
    df_list = read_df_from_folder(folder)
    columns = read_col_from_dataframes(df_list, col_name)
    return columns

def normal_test(data : np.array, test_name):
    """normality test on the numpy array. returns stat, p"""
    sh_names = ['SW','shapiro', 'sh', 'shapiro_wilk', 'shapiro-wilk', 'shapiro-wilk_test', 'shapiro_wilk_test', 'Shapiro', 'Sh', 'Shapiro-Wilk', 'Shapiro-Wilk_test', 'Shapiro_Wilk_test']
    an_names = ['AD','anderson', 'ad', 'anderson-darling', 'anderson_darling', 'anderson-darling_test', 'anderson_darling_test', 'Anderson', 'AD', 'Anderson-Darling', 'Anderson_Darling', 'Anderson-Darling_test', 'Anderson_Darling_test']
    ks_names = ['KS','ks', 'ks2', 'ks_2', 'ks_2samp', 'ks2samp', 'KS', 'KS2', 'KS_2', 'KS_2samp', 'KS2samp', 'Kolmogorov Smirnov','Kolmogorov Smirnov 2 sampled']
    sk_names = ['SK', 'skew', 'sk', 'skewness', 'Skew', 'Sk', 'Skewness', 'kurtosis', 'ku', 'kurt', 'Kurtosis', 'Ku', 'Kurt']
    li_names = ['LF', 'lilliefors', 'lf', 'lilliefors_test', 'LF', 'Lilliefors', 'Lilliefors_test', 'lillie', 'fors', 'Lillie', 'Fors', 'Lillie Fors', 'LF']
    if test_name in sh_names:
        return shapiro_test(data).pvalue
    elif test_name in an_names:
        return anderson_test(data).pvalue
    elif test_name in ks_names:
        return ks_norm_test(data).pvalue
    elif test_name in sk_names:
        return skew_kurtosis_test(data).pvalue
    elif test_name in li_names:
        return lilliefors_test(data)[1]
    else:
        raise ValueError('invalid test name for normal distribution test')

def normal_test_list(data_list : list, test_name):
    """normality test on the numpy arrays in the given list. returns list of [stat, p] in each entry"""
    return [normal_test(data_list[i], test_name) for i in range(0, len(data_list))]

def hypothesis_test(data_1 : np.array, data_2 : np.array, test_name):
    mwu_names = ['mannwhitneyu', 'mwu', 'mw', 'mannwhitney', 'mannwhitney_u', 'MWU', 'MW', 'MannWhitneyU', 'MannWhitney', 'MannWhitney_u', 'Mann Whitney U']
    ks_names = ['ks', 'ks2', 'ks_2', 'ks_2samp', 'ks2samp', 'KS', 'KS2', 'KS_2', 'KS_2samp', 'KS2samp', 'Kolmogorov Smirnov','Kolmogorov Smirnov 2 sampled']
    kw_names = ['kruskalwallis', 'kw', 'kruskalwallis_test', 'KW', 'KruskalWallis', 'kruskal', 'Kruskal', 'Kruskal Wallis']
    bm_names = ['brunnermunzel', 'bm', 'BM', 'BrunnerMunzel', 'brunner', 'munzel', 'Brunner Munzel', 'Brunner']
    bf_names = ['brownforsythe', 'bf', 'brownforsythe_test', 'BF', 'BrownForsythe', 'BrownForsythe_test', 'brown', 'forsythe', 'Brown', 'Forsythe', 'levene', 'Levene', 'Brown Forsythe', 'BF']
    kt_names = ['tau', 'TAU', 'kendallstau', 'kt', 'kendalltau', 'KendallTau', 'KendallTau_test', 'Kendall', 'Tau', 'Kendall Tau', 'KT']
    sr_names = ['spearmanr', 'sr', 'spearman', 'Spearman', 'SpearmanR', 'SpearmanR_test', 'Spearman R', 'SR']
                
    if test_name in mwu_names:
        return mannwhitneyu_test(data_1, data_2)
    elif test_name in ks_names:
        return ks_2samp(data_1, data_2)
    elif test_name in kw_names:
        return kruskalwallis_test(data_1, data_2)
    elif test_name in bm_names:
        return brunnermunzel_test(data_1, data_2)
    elif test_name in bf_names:
        return brownforsythe_test(data_1, data_2)
    elif test_name in kt_names:
        return kendallstau(data_1, data_2)
    elif test_name in sr_names:
        return spearmanr(data_1, data_2)
    else:
        raise ValueError('invalid test name for hypothesis test')
    
def hypothesis_test_list(data_list_1 : list, data_list_2 : list, test_name):
    """hypothesis test on the numpy arrays in the two given lists (pairwise with same index). returns list of [stat, p] in each entry"""
    return [hypothesis_test(data_list_1[i], data_list_2[i], test_name).pvalue for i in range(0, len(data_list_1))]

def correlation_value(data_1 : np.array, data_2 : np.array, correlation_name):
    """computes the correlation value for the two numpy arrays. returns correlation value"""
    if correlation_name == 'f':
        return f_value_mwu(data_1, data_2)
    elif correlation_name == 'r':
        return r_values_mwu(data_1, data_2)
    else:
        raise ValueError('invalid correlation name for correlation value')

def correlation_value_list(data_list_1 : list, data_list_2 : list, correlation_name):
    """computes the correlation value for each pair of numpy arrays in the two given lists (pairwise with same index). returns list of correlation values"""
    return [correlation_value(data_list_1[i], data_list_2[i], correlation_name) for i in range(0, len(data_list_1))]
    
def folder_names_from_folder_paths(folders):
    """derives column names from the folder names."""
    return [name.split('/')[-1].split('_',1)[1].replace('_','\_') for name in folders]