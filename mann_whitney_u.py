import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from util_hypothesis_tests import *

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