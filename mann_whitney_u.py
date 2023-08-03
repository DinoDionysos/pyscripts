import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys

# read the two csv files from the command line
df_1 = pd.read_csv(sys.argv[1])
df_2 = pd.read_csv(sys.argv[2])

# calculate x_diff by x_data - x_gt
df_1['x_diff'] = df_1['x_data'] - df_1['x_gt']
df_2['x_diff'] = df_2['x_data'] - df_2['x_gt']
# calculate y_diff by y_data - y_gt
df_1['y_diff'] = df_1['y_data'] - df_1['y_gt']
df_2['y_diff'] = df_2['y_data'] - df_2['y_gt']
# calculate euclidean distance by sqrt(x_diff^2 + y_diff^2)
df_1['euclidean_distance'] = ((df_1['x_diff'])**2 + (df_1['y_diff'])**2)**0.5
df_2['euclidean_distance'] = ((df_2['x_diff'])**2 + (df_2['y_diff'])**2)**0.5


# def function called S(a,b)
def S(a,b):
    if a > b:
        return 1
    elif a == b:
        return 0.5
    elif a < b:
        return 0
#def a function name mwu_statistic
def mwu_statistic(data_1, data_2):
    sum = 0 
    for i in range(len(data_1)):
        for j in range(len(data_2)):
            sum += S(data_1[i], data_2[j])
    return sum

distances_1 = df_1['euclidean_distance'].to_numpy()
distances_2 = df_2['euclidean_distance'].to_numpy()

print('self calculated mwu statistic')
print('Statistics 1 = %.3f \nStatistics 2 = %.3f' %(mwu_statistic(distances_1, distances_2),mwu_statistic(distances_2, distances_1)))
print('--------------------------------------------------')
#perform a mann whitney u test
from scipy.stats import mannwhitneyu
stat_x, p = mannwhitneyu(distances_1, distances_2, alternative ='two-sided')
stat_y = distances_1.shape[0] * distances_2.shape[0] - stat_x
print('Statistics 1 = %.3f \nStatistics 2 = %.3f \np=%.3f' % (stat_x, stat_y, p))

# interpret
alpha = 0.05
if p > alpha:
    print('Same distribution (fail to reject H0)')
else:
    print('Different distribution (reject H0)')

print('--------------------------------------------------')
temp = distances_1
distances_1 = distances_2
distances_2 = temp
del temp
stat_x, p = mannwhitneyu(distances_1, distances_2, alternative ='two-sided')
stat_y = distances_1.shape[0] * distances_2.shape[0] - stat_x
print('Statistics 1 = %.3f \nStatistics 2 = %.3f \np=%.3f' % (stat_x, stat_y, p))

# interpret
alpha = 0.05
if p > alpha:
    print('Same distribution (fail to reject H0)')
else:
    print('Different distribution (reject H0)')