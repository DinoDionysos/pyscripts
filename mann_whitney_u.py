import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys



# read the two csv files from the command line
df_1 = pd.read_csv(sys.argv[1])
df_2 = pd.read_csv(sys.argv[2])

factor_meter = 1000
df_1['x'] *= factor_meter 
df_1['y'] *= factor_meter
df_1['x_gt'] *= factor_meter
df_1['y_gt'] *= factor_meter
df_2['x'] *= factor_meter
df_2['y'] *= factor_meter
df_2['x_gt'] *= factor_meter
df_2['y_gt'] *= factor_meter

# calculate x_diff by x - x_gt
df_1['x_diff'] = df_1['x'] - df_1['x_gt']
df_2['x_diff'] = df_2['x'] - df_2['x_gt']
# calculate y_diff by y - y_gt
df_1['y_diff'] = df_1['y'] - df_1['y_gt']
df_2['y_diff'] = df_2['y'] - df_2['y_gt']
# calculate euclidean distance by sqrt(x_diff^2 + y_diff^2)
df_1['euclidean_distance'] = ((df_1['x_diff'])**2 + (df_1['y_diff'])**2)**0.5
df_2['euclidean_distance'] = ((df_2['x_diff'])**2 + (df_2['y_diff'])**2)**0.5
# calculate the first discrete difference of the euclidean_distance column
df_1['euclidean_distance_delta'] = df_1['euclidean_distance'].diff()
df_2['euclidean_distance_delta'] = df_2['euclidean_distance'].diff()

def S(a,b):
    if a > b:
        return 1
    elif a == b:
        return 0.5
    elif a < b:
        return 0

def mwu_statistic(data_1, data_2):
    sum = 0 
    for i in range(len(data_1)):
        for j in range(len(data_2)):
            sum += S(data_1[i], data_2[j])
    return sum

distances_1 = df_1['euclidean_distance'].to_numpy()
distances_2 = df_2['euclidean_distance'].to_numpy()
# make in mm
distances_1 = distances_1
distances_2 = distances_2
# drop the first row of both dataframes (0 or nan in both cases)
distances_1 = distances_1[1:]
distances_2 = distances_2[1:]
# shorten both distances to 700
# distances_1 = distances_1[:700]
# distances_2 = distances_2[:700]
# cut of everything bigger than the variance
# distances_1 = distances_1[distances_1 < np.var(distances_1)]
# distances_2 = distances_2[distances_2 < np.var(distances_2)]
print('variance of distances_1 = %.15f' % np.var(distances_1))
print('variance of distances_2 = %.15f' % np.var(distances_2))
print('standard deviation of distances_1 = %.15f' % np.std(distances_1))
print('standard deviation of distances_2 = %.15f' % np.std(distances_2))
print('mean of distances_1 = %.15f' % np.mean(distances_1))
print('mean of distances_2 = %.15f' % np.mean(distances_2))
print('median of distances_1 = %.15f' % np.median(distances_1))
print('median of distances_2 = %.15f' % np.median(distances_2))
print('--------------------------------------------------')
# remove outlier bigger than 0.025 and smaller than -0.025
# distances_1 = distances_1[distances_1 < 0.025]
# distances_1 = distances_1[distances_1 > -0.025]
# distances_2 = distances_2[distances_2 < 0.025]
# distances_2 = distances_2[distances_2 > -0.025]
# cut distances from 650 to -120
distances_1 = distances_1[650:-120]
distances_2 = distances_2[650:-120]






print('self calculated mwu statistic')
print('Statistics 1 = %.3f \nStatistics 2 = %.3f' %(mwu_statistic(distances_1, distances_2),mwu_statistic(distances_2, distances_1)))
print('--------------------------------------------------')
#perform a mann whitney u test
from scipy.stats import mannwhitneyu
stat_x, p = mannwhitneyu(distances_1, distances_2, alternative ='two-sided')
stat_y = distances_1.shape[0] * distances_2.shape[0] - stat_x
print('mwu Statistics 1 = %.1f \nmwu Statistics 2 = %.1f \np=%.15f' % (stat_x, stat_y, p))

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
print('mwu Statistics 1 = %.1f \nmwu Statistics 2 = %.1f \np=%.15f' % (stat_x, stat_y, p))

# interpret
alpha = 0.05
if p > alpha:
    print('Same distribution (fail to reject H0)')
else:
    print('Different distribution (reject H0)')

# kologorov smirnov test
print('--------------------------------------------------')
from scipy.stats import ks_2samp
stat, p = ks_2samp(distances_1, distances_2)
print('KS Statistics=%.3f \np=%.15f' % (stat, p))
# interpret
alpha = 0.05
if p > alpha:
    print('Same distribution (fail to reject H0)')
else:
    print('Different distribution (reject H0)')

