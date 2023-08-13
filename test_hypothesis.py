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
        dist_list_2 (list of arrays): The second data sets to compare with.
        alpha (float): alpha value of the tests
        print_every=True (bool): print results or not 
 
    Returns:
        pmean_mwu_test (float): mean of all the p values
        pvalues_mwu_test (list of float): all the p values of the kolomogorov smirnov  tests
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