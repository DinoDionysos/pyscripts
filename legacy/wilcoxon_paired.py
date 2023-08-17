import pandas as pd
import numpy as np
import sys

# read the two csv files from the command line
df_1 = pd.read_csv(sys.argv[1])
df_2 = pd.read_csv(sys.argv[2])

# turn into numpy array x, y and x_gt, y_gt and stamp
x_1 = df_1['x'].to_numpy()
y_1 = df_1['y'].to_numpy()
x_gt_1 = df_1['x_gt'].to_numpy()
y_gt_1 = df_1['y_gt'].to_numpy()
stamp_1 = df_1['stamp'].to_numpy()
x_2 = df_2['x'].to_numpy()
y_2 = df_2['y'].to_numpy()
x_gt_2 = df_2['x_gt'].to_numpy()
y_gt_2 = df_2['y_gt'].to_numpy()
stamp_2 = df_2['stamp'].to_numpy()

#interpolate the second such that it has the same length as the first
x_2 = np.interp(stamp_1, stamp_2, x_2)
y_2 = np.interp(stamp_1, stamp_2, y_2)

# calculate the diff of both to the ground truth of df_1
x_diff_1 = x_1 - x_gt_1
y_diff_1 = y_1 - y_gt_1
x_diff_2 = x_2 - x_gt_1
y_diff_2 = y_2 - y_gt_1

# calculate the euclidean distance of both to the ground truth of df_1
euclidean_distance_1 = ((x_diff_1)**2 + (y_diff_1)**2)**0.5
euclidean_distance_2 = ((x_diff_2)**2 + (y_diff_2)**2)**0.5
#calculate the first discrete difference of the euclidean distance
euclidean_distance_delta_1 = euclidean_distance_1[1:] - euclidean_distance_1[:-1]
euclidean_distance_delta_2 = euclidean_distance_2[1:] - euclidean_distance_2[:-1]


# do a signed rank wilcoxon test
# from scipy.stats import wilcoxon
# stat_x, p_x = wilcoxon(euclidean_distance_delta_1, euclidean_distance_delta_2, alternative ='two-sided')
# print('Statistics = %.1f \np=%.15f' % (stat_x, p_x))

# do a median test
from scipy.stats import median_test
stat_x, p_x, med, tbl = median_test(euclidean_distance_1, euclidean_distance_2)
# print all of the results
print('Statistics = %.1f \np=%.15f \nmed=%.3f \ntbl=%s' % (stat_x, p_x, med, tbl))




