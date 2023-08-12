import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

#input
# 1: folder path with rotated csv files
# 3: threshold, where to split the csv files in two groups

folder_1 = sys.argv[1]
thresh_1 = int(sys.argv[2])

df_list_1 = []
df_list_2 = []

# get all the names of the csv in the folder and read them in
count = 0
for filename in os.listdir(folder_1):
    if count < thresh_1:
        if filename.endswith('.csv'):
            df_list_1.append(pd.read_csv(os.path.join(folder_1, filename)))
    else:
        if filename.endswith('.csv'):
            df_list_2.append(pd.read_csv(os.path.join(folder_1, filename)))
            pass
    count += 1

from scipy.stats import mannwhitneyu
alpha_mwu = 0.05
pvalues_mwu_test = []
for i in range(0, int(thresh_1)):
    distances_1 = df_list_1[i]['dist'].to_numpy()
    distances_2 = df_list_2[i]['dist'].to_numpy()
    #perform a mann whitney u test and print the results
    stat_x, p = mannwhitneyu(distances_1, distances_2, alternative ='two-sided')
    pvalues_mwu_test.append(p)
    stat_y = distances_1.shape[0] * distances_2.shape[0] - stat_x
    print('mwu stat 1 = %.1f, stat 2 = %.1f, p=%.15f'.ljust(50) % (stat_x, stat_y, p), end='')
    if p > alpha_mwu:
        print('Same distribution (fail to reject H0) pvalue=%d' % p)
    else:
        print('Different distribution (reject H0) pvalue=%d' % p)
pmean_mwu_test = np.mean(pvalues_mwu_test)
print('mean pvalue = %.15f' % pmean_mwu_test)
# print hello without newline after
print('hello', end='')

# alpha_ks = 0.05
# pvalues_ks_test = []
# for i in range(int(range_1), int(range_2)):
#     distances_1 = df_list_1[i]['euclidean_distance'].to_numpy()
#     distances_2 = df_list_2[i]['euclidean_distance'].to_numpy()
#     # kologorov smirnov test
#     print('--------------------------------------------------')
#     from scipy.stats import ks_2samp
#     stat, p = ks_2samp(distances_1, distances_2)
#     pvalues_ks_test.append(p)
#     print('KS Statistics=%.3f, p=%.15f' % (stat, p), end='')
#     if p > alpha_ks:
#         print('Same distribution (fail to reject H0)')
#     else:
#         print('Different distribution (reject H0)')
# pmean_ks_test = np.mean(pvalues_ks_test)
# print('mean pvalue = %.15f' % pmean_ks_test)



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