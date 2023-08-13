#!/usr/bin/python3
import numpy as np
from scipy.stats import mannwhitneyu
from scipy.stats import ks_2samp


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
        print('mwu stat 1 = %.1f, p=%.15f' % (stat_x, p), end='')
        if p > alpha:
            print('Same distribution (fail to reject H0) pvalue=%d' % p)
        else:
            print('Different distribution (reject H0) pvalue=%.15f' % p)
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
    print('mean pvalue = %.15f ' % pmean_mwu_test)
    return pmean_mwu_test, pvalues_mwu_test

def kolomogorov_print(data_1, data_2, alpha, print_res=True):
    """
    perform a kolomogorov smirnov test.
    prints the results if print_res=True.
 
    Args:
        dist_1 (array int): The first data set.
        dist_2 (array int): The second data set to compare with.
        alpha (float): alpha value of the test
        print_res=True (bool): print results or not 
 
    Returns:
        stat (float): test statistic of kolomogorov smirnov test
        p (float): p values of kolomogorov smirnov test
    """
    #
    stat, p = ks_2samp(data_1, data_2)
    if print_res == True:
        print('ks stat 1 = %.1f, p=%.15f' % (stat, p), end='')
        if p > alpha:
            print('Same distribution (fail to reject H0) pvalue=%d' % p)
        else:
            print('Different distribution (reject H0) pvalue=%.15f' % p)
    return stat, p

def kolomogorov_n(dist_list_1, dist_list_2, alpha, print_every=True):
    """
    perform a two sided kolomogorov smirnov test on every array with the same index given in dist_list_1 and dist_list_2. Then takes the mean of the p values and prints them
    prints all the results of the pairwise tests, if print_res=True.
 
    Args:
        dist_list_1 (list of arrays): The first data sets.
        dist_list_2 (list of arrays): The second data set to compare with.
        alpha (float): alpha value of the tests
        print_every=True (bool): print results or not 
 
    Returns:
        pmean_mwu_test (float): mean of all the p values
        pvalues_mwu_test (list of float): all the p values of the kolomogorov smirnov tests
    """
    assert len(dist_list_1) == len(dist_list_2), "length of lists are not the same: length 1 = {len(dist_list_1)}, length 2 = len(dist_list_2) "
    pvalues_mwu_test = []
    for i in range(0, len(dist_list_1)):
        if print_every:
            print(i," ", end='')
        stat, p = kolomogorov_print(dist_list_1[i], dist_list_2[i], alpha, print_every)
        pvalues_mwu_test.append(p) 
    pmean_mwu_test = np.mean(pvalues_mwu_test)
    print('mean pvalue = %.15f ' % pmean_mwu_test)
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
            pmean, pvalues = kolomogorov_n(columns[0:len_cols_half], columns[len_cols_half:2*len_cols_half], alpha, print_every=print_every)
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
            pmean, pvalues = kolomogorov_n(columns_1, columns_2, alpha, print_every=print_every)
        return pmean, pvalues

def mean_hypo(test_name, csv_folders, col_name, alpha,print_every=True):
    """
    takes a test name and tests the data in the csv folders against each other. returns the rsults in a numpy array.
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