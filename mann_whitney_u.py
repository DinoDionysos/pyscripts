import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from util_hypothesis_tests import *




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


folders = ["csv/aligned/c8_orb_stereo", "csv/aligned/c8_orb_d435"]
folder_save = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/results/"
test_name = "mwu"
col_name = 'dist'
alpha = 0.05
print_every = True
pmean_values, pvalues = mean_hypo(test_name, folders, col_name, alpha, print_every)

column_names = []
for name in folders:
    column_names.append(name.split('/')[-1].split('_',1)[1].replace('_','\_'))
df = pd.DataFrame(pmean_values, columns = column_names, index=column_names)

caption = "mean p values over 20 experiments for the mann whitney u test"
label = "tab:mean_pvalues_mwu"
precision = 6
# df_latex_2 = df.style.to_latex(
#     hrules=True,
#     position_float="centering",
#     caption=caption,
#     label=label)
# with open(folder_save+'result_pmean_2.tex', 'w') as f:
#     f.write(df_latex_2)
# print(df_latex_2)

# take the dataframe df and make a latex table out of it
df_latex = "\centering\n"
df_latex += df.to_latex(header=True, float_format=f"%.{precision}f", index=True)
df_latex = df_latex.replace('-1.' + '0' * precision, '-')
# append the caption and label to the latex table string
df_latex += "\caption{"+caption+"}\n\label{"+label+"}\n"
with open(folder_save+'result_pmean.tex', 'w') as f:
    f.write(df_latex)
# print(df_latex)

# take pvalues and make a latex table out of it
caption = "p values for the mann whitney u test"
label = "tab:pvalues_mwu"
precision = 6
pvalues = np.array(pvalues)
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

df_pvalues_latex = "\centering\n"
df_pvalues_latex += df_pvalues.to_latex(header=True, float_format=f"%.{precision}f", index=True)
# replace all the occurences of -1 with a dash
df_pvalues_latex = df_pvalues_latex.replace('-1.' + '0' * precision, '-')
df_pvalues_latex = df_pvalues_latex.replace('\nmean &', '\n\midrule\nmean &')
df_pvalues_latex += "\caption{"+caption+"}\n\label{"+label+"}\n"
with open(folder_save+'result_pvalues.tex', 'w') as f:
    f.write(df_pvalues_latex)
print(df_pvalues_latex)

sys.exit(1)


#input
# 1: folder path with rotated csv files
# 2: folder path with rotated csv files to compare with
# 3: range start to compare pairwise folder_1 and folder_2
# 3: range end to compare pairwise folder_1 and folder_2

folder_1 = sys.argv[1]
folder_2 = sys.argv[2]
range_1 = int(sys.argv[3])
range_2 = int(sys.argv[4])



df_list_1 = []
df_list_2 = []

# get all the names of the csv in the folder and read them in
for filename in os.listdir(folder_1):
    if filename.endswith('.csv'):
        df_list_1.append(pd.read_csv(os.path.join(folder_1, filename)))
for filename in os.listdir(folder_2):
    if filename.endswith('.csv'):
        df_list_2.append(pd.read_csv(os.path.join(folder_2, filename)))

from util_hypothesis_tests import *
alpha_mwu = 0.05
# convert the column 'dist' of df_list_1 to numpy and save it in another list for every entry
distances_1 = []
distances_2 = []
for j in range(range_1,range_2):
    distances_1.append(df_list_1[j]['dist'].to_numpy())
    distances_2.append(df_list_2[j]['dist'].to_numpy())

pmean_mwu_test, pvalues_mwu_test = mannwhitneyu_n(distances_1, distances_2, alpha_mwu, print_every=True)
print('mean pvalue = %.15f ' % pmean_mwu_test)

# make dataframe from pvalues_mwu_test


# df_data = pd.DataFrame({'pvalue': pvalues_mwu_test})
# print(df_data)
# for i in range(int(range_1), int(range_2)):
#     distances_1 = df_list_1[i]['dist'].to_numpy()
#     distances_2 = df_list_2[i]['dist'].to_numpy()
#     #perform a mann whitney u test and print the results
#     stat_x, p = mannwhitneyu(distances_1, distances_2, alternative ='two-sided')
#     pvalues_mwu_test.append(p)
#     stat_y = distances_1.shape[0] * distances_2.shape[0] - stat_x
#     print('mwu stat 1 = %.1f, stat 2 = %.1f, p=%.15f' % (stat_x, stat_y, p), end='')
#     if p > alpha_mwu:
#         print('Same distribution (fail to reject H0) pvalue=%d' % p)
#     else:
#         print('Different distribution (reject H0) pvalue=%.15f' % p)
# pmean_mwu_test = np.mean(pvalues_mwu_test)
# print('mean pvalue = %.15f ' % pmean_mwu_test)

# alpha_ks = 0.05
# pvalues_ks_test = []
# for i in range(int(range_1), int(range_2)):
#     distances_1 = df_list_1[i]['dist'].to_numpy()
#     distances_2 = df_list_2[i]['dist'].to_numpy()
#     # kologorov smirnov test
#     from scipy.stats import ks_2samp
#     stat, p = ks_2samp(distances_1, distances_2)
#     pvalues_ks_test.append(p)
#     print('KS Statistics=%.3f, p=%.15f' % (stat, p), end='')
#     if p > alpha_ks:
#         print('Same distribution (fail to reject H0)')
#     else:
#         print('Different distribution (reject H0)')
# pmean_ks_test = np.mean(pvalues_ks_test)
# print('mean pvalue = %.15f ' % pmean_ks_test)



# def S(a,b):
#     if a > b:
#         return 1
#     elif a == b:
#         return 0.5
#     elif a < b:
#         return 0

# def mwu_statistic(data_1, data_2):
#     sum = 0 
#     for i in range(len(data_1)):
#         for j in range(len(data_2)):
#             sum += S(data_1[i], data_2[j])
#     return sum

# print('self calculated mwu statistic')
# print('Statistics 1 = %.3f \nStatistics 2 = %.3f' %(mwu_statistic(distances_1, distances_2),mwu_statistic(distances_2, distances_1)))
# print('--------------------------------------------------')

# print('--------------------------------------------------')
# print('variance of distances_1 = %.15f' % np.var(distances_1))
# print('variance of distances_2 = %.15f' % np.var(distances_2))
# print('standard deviation of distances_1 = %.15f' % np.std(distances_1))
# print('standard deviation of distances_2 = %.15f' % np.std(distances_2))
# print('mean of distances_1 = %.15f' % np.mean(distances_1))
# print('mean of distances_2 = %.15f' % np.mean(distances_2))
# print('median of distances_1 = %.15f' % np.median(distances_1))
# print('median of distances_2 = %.15f' % np.median(distances_2))
# print('--------------------------------------------------')
# remove outlier bigger than 0.025 and smaller than -0.025
# distances_1 = distances_1[distances_1 < 0.025]
# distances_1 = distances_1[distances_1 > -0.025]
# distances_2 = distances_2[distances_2 < 0.025]
# distances_2 = distances_2[distances_2 > -0.025]
# cut distances from 650 to -120
# distances_1 = distances_1[650:-120]
# distances_2 = distances_2[650:-120]