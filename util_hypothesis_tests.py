#!/usr/bin/python3
import numpy as np
from scipy.stats import mannwhitneyu
from scipy.stats import ks_2samp
import os
import pandas as pd



def mannwhitneyu_print(data_1, data_2, alpha, print_res=True):
    """
    perform a two sided mann whitney u test.
    prints the results if print_res=True.
 
    Args:
        dist_1 (array int): The first data set.
        dist_2 (array int): The second data set to compare with.
        alpha (float): alpha value of the test
        print_res=True (bool): print results or not 
 
    Returns:
        stat_x (float): test statistic of mann whitney u test
        p (float): p values of mann whitney u test
    """
    #
    stat_x, p = mannwhitneyu(data_1, data_2, alternative ='two-sided')
    if print_res == True:
        print('mwu stat 1 = %.1f, p=%.6f' % (stat_x, p), end='')
        if p > alpha:
            print('Same distribution (fail to reject H0) pvalue=%d' % p)
        else:
            print('Different distribution (reject H0) pvalue=%.6f' % p)
    return stat_x, p

def mannwhitneyu_n(dist_list_1, dist_list_2, alpha, print_every=True):
    """
    perform a two sided mann whitney u test on every array with the same index given in dist_list_1 and dist_list_2. Then takes the mean of the p values and prints them.
    prints all the results of the pairwise tests, if print_res=True.
 
    Args:
        dist_list_1 (list of arrays): The first data sets.
        dist_list_2 (list of arrays): The second data sets to compare with.
        alpha (float): alpha value of the tests
        print_every=True (bool): print results or not 
 
    Returns:
        pmean_mwu_test (float): mean of all the p values
        pvalues_mwu_test (list of float): all the p values of the mann whitney u tests
    """
    assert len(dist_list_1) == len(dist_list_2), f"length of lists are not the same: length 1 = {len(dist_list_1)}, length 2 = {len(dist_list_2)} "
    pvalues_mwu_test = []
    for i in range(0, len(dist_list_1)):
        if print_every:
            print(i," ", end='')
        stat, p = mannwhitneyu_print(dist_list_1[i], dist_list_2[i], alpha, print_every)
        pvalues_mwu_test.append(p) 
    pmean_mwu_test = np.mean(pvalues_mwu_test)
    print('mean pvalue = %.6f ' % pmean_mwu_test)
    return pmean_mwu_test, pvalues_mwu_test

def kolmogorov_print(data_1, data_2, alpha, print_res=True):
    """
    perform a kolmogorov smirnov test.
    prints the results if print_res=True.
 
    Args:
        dist_1 (array int): The first data set.
        dist_2 (array int): The second data set to compare with.
        alpha (float): alpha value of the test
        print_res=True (bool): print results or not 
 
    Returns:
        stat (float): test statistic of kolmogorov smirnov test
        p (float): p values of kolmogorov smirnov test
    """
    #
    stat, p = ks_2samp(data_1, data_2)
    if print_res == True:
        print('ks stat 1 = %.1f, p=%.6f' % (stat, p), end='')
        if p > alpha:
            print('Same distribution (fail to reject H0) pvalue=%d' % p)
        else:
            print('Different distribution (reject H0) pvalue=%.6f' % p)
    return stat, p

def kolmogorov_n(dist_list_1, dist_list_2, alpha, print_every=True):
    """
    perform a two sided kolmogorov smirnov test on every array with the same index given in dist_list_1 and dist_list_2. Then takes the mean of the p values and prints them
    prints all the results of the pairwise tests, if print_res=True.
 
    Args:
        dist_list_1 (list of arrays): The first data sets.
        dist_list_2 (list of arrays): The second data set to compare with.
        alpha (float): alpha value of the tests
        print_every=True (bool): print results or not 
 
    Returns:
        pmean_mwu_test (float): mean of all the p values
        pvalues_mwu_test (list of float): all the p values of the kolmogorov smirnov tests
    """
    assert len(dist_list_1) == len(dist_list_2), "length of lists are not the same: length 1 = {len(dist_list_1)}, length 2 = len(dist_list_2) "
    pvalues_mwu_test = []
    for i in range(0, len(dist_list_1)):
        if print_every:
            print(i," ", end='')
        stat, p = kolmogorov_print(dist_list_1[i], dist_list_2[i], alpha, print_every)
        pvalues_mwu_test.append(p) 
    pmean_mwu_test = np.mean(pvalues_mwu_test)
    print('mean pvalue = %.6f ' % pmean_mwu_test)
    return pmean_mwu_test, pvalues_mwu_test

def read_csv_from_folder(folder):
    """reads all the csv in the folder into a list of dataframes"""
    df_list = []
    for filename in os.listdir(folder):
        if filename.endswith('.csv'):
            df_list.append(pd.read_csv(os.path.join(folder, filename)))
    return df_list

def read_col_from_dataframes(df_list, col_name):
    """reads a certain column (f.e. 'dist') from all the dataframes in the df_list and returns them as a list of numpy arrays"""
    columns = []
    for j in range(0, len(df_list)):
        columns.append(df_list[j][col_name].to_numpy())
    return columns

def read_col_from_folder(folder, col_name):
    """reads a certain column from all the csv in the folder and returns them as a list of arrays"""
    df_list = read_csv_from_folder(folder)
    columns = read_col_from_dataframes(df_list, col_name)
    return columns

def hypotest_folder(test_name, folder_1, folder_2, col_name, alpha, print_every=True):
    """Takes in two folders. Extracts from them a certain column of every csv that is in the the folders. Then compares the two cols with the same index from the two folders. If both folder are the same, one half is compared to the other half. returns the mean p value and the list of the p values. """
    auto = folder_1 == folder_2
    if auto:
        print("same folders ",folder_1, folder_2)
        columns = read_col_from_folder(folder_1, col_name)
        len_cols_half = int(len(columns)/2)
        if test_name == "mwu" or test_name == "mannwhitneyu":
            pmean, pvalues = mannwhitneyu_n(columns[0:len_cols_half], columns[len_cols_half:2*len_cols_half], alpha, print_every=print_every)
        elif test_name == "ks" or test_name == "kstest" or test_name == "kolmogorov":
            pmean, pvalues = kolmogorov_n(columns[0:len_cols_half], columns[len_cols_half:2*len_cols_half], alpha, print_every=print_every)
        else:
            print("hypotest_folder(...): test_name not recognized. default to kolmogorov")
            pmean, pvalues = kolmogorov_n(columns[0:len_cols_half], columns[len_cols_half:2*len_cols_half], alpha, print_every=print_every)
        # append some -1 to the pvalues list to make it the same length as the columns list
        pvalues = np.append(pvalues, (-1) * np.ones(len(columns)-len_cols_half))
        return pmean, pvalues
    else:
        print("different folders ",folder_1, folder_2)
        columns_1 = read_col_from_folder(folder_1, col_name)
        columns_2 = read_col_from_folder(folder_2, col_name)
        if test_name == "mwu" or test_name == "mannwhitneyu":
            pmean, pvalues = mannwhitneyu_n(columns_1, columns_2, alpha, print_every=print_every)
        elif test_name == "ks" or test_name == "kstest" or test_name == "kolmogorov":
            pmean, pvalues = kolmogorov_n(columns_1, columns_2, alpha, print_every=print_every)
        else:
            print("hypotest_folder(...): test_name not recognized. default to kolmogorov")
            pmean, pvalues = kolmogorov_n(columns_1, columns_2, alpha, print_every=print_every)
        return pmean, pvalues

def mean_hypo(test_name, csv_folders, col_name, alpha,print_every=True):
    """
    takes a test name and tests the data in the csv folders against each other. returns the results in a numpy array.
    """
    num_folders = len(csv_folders)
    pmean_values = (-1) * np.ones((num_folders, num_folders))
    pvalues_list = []
    for i in range(0, num_folders):
        for j in range(0, num_folders):
            if j > i: 
                break
            pmean, pvalues= hypotest_folder(test_name, csv_folders[i],csv_folders[j],col_name,alpha,print_every=print_every)
            pmean_values[j][i] = -1
            pmean_values[i][j] = pmean
            pvalues_list.append(pvalues)
    return pmean_values, pvalues_list

def make_mean_table(df, folder_save, test_name, col_name, caption, label, precision=6, save=True):
    """takes the mean values from the experiments as dataframe and turns it into a latex table."""
    # take the mean p values and make a latex table out of it
    df_latex = "\centering\n"
    df_latex += df.to_latex(header=True, float_format=f"%.{precision}f", index=True)
    df_latex = df_latex.replace('-1.' + '0' * precision, '-')
    # append the caption and label to the latex table string
    df_latex += "\caption{"+caption+"}\n\label{"+label+"}\n"
    if save:
        with open(folder_save+f'result_pmean_{test_name}_{col_name}.tex', 'w') as f:
            f.write(df_latex)
    return df_latex

def make_pvalues_table(df, folder_save, test_name, col_name, caption, label, precision=6, save=True):
    """takes all the pvalues in a dataframe and makes a latex table out of it."""
    df_latex = "\centering\n"
    df_latex += df.to_latex(header=True, float_format=f"%.{precision}f", index=True)
    df_latex = df_latex.replace('-1.' + '0' * precision, '-')
    df_latex = df_latex.replace('\nmean &', '\n\midrule\nmean &')
    # append the caption and label to the latex table string
    df_latex += "\caption{"+caption+"}\n\label{"+label+"}\n"
    if save:
        with open(folder_save+f'result_pvalues_{test_name}_{col_name}.tex', 'w') as f:
            f.write(df_latex)
    return df_latex

def make_pvalues_df(pvalues, pmean_values, folders, alpha):
    """takes the pvalues and makes a dataframe. the dataframe is designed to be converted into a latex table."""
    df_pvalues = pd.DataFrame()
    # for every entry of pvalues, make a new column in the dataframe
    for i in range(0, len(pvalues)):
        df_pvalues[str(i)] = pvalues[i]
    df_pvalues.columns = ['stereo stereo', 'stereo rgbd', 'rgbd rgbd'] 
    # add a row at the bottom with the mean of the pvalues
    pmean_values_flat = []
    for i in range(0, len(folders)):
        for j in range(0, len(folders)):
            if i < j: 
                break
            pmean_values_flat.append(pmean_values[i][j])
    df_pvalues.loc['mean'] = pmean_values_flat
    # make another row with if mean is > alpha than say 'rejected' else 'failed to reject'
    rejected = df_pvalues.loc['mean'] < alpha
    rejected = rejected.replace(True, 'rejected')
    rejected = rejected.replace(False, 'failed')
    df_pvalues.loc['result'] = rejected
    return df_pvalues

def col_names_from_folders(folders):
    """derives column names from the folder names."""
    column_names = []
    for name in folders:
        column_names.append(name.split('/')[-1].split('_',1)[1].replace('_','\_'))
    return column_names

def make_tables_from_experiment(folder_save, test_name, col_name, folders, alpha, precision=6, print_every=True):
    """takes a several experiments in their folders, performs a hypothesis test on them and makes a latex table."""
    caption = f"mean p values over 20 experiments for the {test_name} test on {col_name}"
    label = f"tab:mean_pvalues_{test_name}_{col_name}"
    column_names = col_names_from_folders(folders)

    pmean_values, pvalues = mean_hypo(test_name, folders, col_name, alpha, 
    print_every = print_every)
    df = pd.DataFrame(pmean_values, columns = column_names, index=column_names)
    # take the mean p values and make a latex table out of it and save it
    df_mean_latex = make_mean_table(df, folder_save, test_name, col_name, caption, label, precision, save=True)

    # take pvalues and make a latex table out of it
    caption = f"p values for the {test_name} test on {col_name}"
    label = f"tab:pvalues_{test_name}_{col_name}"
    pvalues = np.array(pvalues)
    df_pvalues = make_pvalues_df(pvalues, pmean_values, folders, alpha)

    # make a latex table out of it
    df_pvalues_latex = make_pvalues_table(df_pvalues, folder_save, test_name, col_name, caption, label, precision, save=True)
    return df_mean_latex, df_pvalues_latex