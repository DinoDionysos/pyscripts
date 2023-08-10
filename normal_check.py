import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import stats
# import statsmodels.api as sm

from statsmodels.stats.diagnostic import lilliefors



folder_1 = "/home/dino/figures"
folder_2 = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/figures"
save_name = 'c4_orb_s1_d1'
save_name_fig_1 = save_name + '_hist_eucl.pdf'
save_name_fig_2 = save_name + '_hist_xy.pdf'
save_name_fig_3 = save_name + '_over_time.pdf'

fontsize_xlabel = 14
fontsize_ylabel = fontsize_xlabel
labelsize_axes = 13
fontsize_title = 16
fontsize_legend = 12
fontsize_legend_time = fontsize_legend
linewidth_gt = 2
linewidth_data = 2
suptitle = 'ORB SLAM3 stereo and ORB SLAM3 rgbd' # overall title on the very top
color_list = ['red', 'black', 'blue', 'green', 'orange', 'purple', 'pink', 'cyan', 'yellow']
df_type_list_overwrite = ['stereo', 'rgb'] # leaf blank if no overwrite

bins_x_number = 50
bins_y_number = bins_x_number
bins_x = np.linspace(-0.15,0.15,bins_x_number)
bins_y = np.linspace(-0.1,0.1,bins_y_number)

bins_euclidean_number = 50
bins_euclidean_delta_number = 200 
bins_euclidean = np.linspace(0,0.15,bins_euclidean_number)
bins_euclidean_delta = np.linspace(-0.1,0.1,bins_euclidean_delta_number)



plt.rc('axes', axisbelow=True)

df_list = []
df_type_list = df_type_list_overwrite
df_type_name_list = ['ground_truth', 'mono', 'stereo', 'd435', 'unknown']
# import arbitrary number of csv files from csv/aligned
for i in range(1, len(sys.argv)):
    df_list.append(pd.read_csv(sys.argv[i]))
    # split at _vs_ and take the last part
    last_part_of_arg = sys.argv[i].split('_vs_')[-1]
    last_part_of_arg = last_part_of_arg.replace('.csv', '')
    last_part_of_arg = last_part_of_arg.replace('-bag', '')
    df_type_list.append(last_part_of_arg)


# calculate the euclidean distance between the ground truth and the data without z
for i in range(len(df_list)):
    df_list[i]['euclidean_distance'] = ((df_list[i]['x'] - df_list[i]['x_gt'])**2 + (df_list[i]['y'] - df_list[i]['y_gt'])**2)**0.5
    # diff too
    df_list[i]['euclidean_distance_delta'] = df_list[i]['euclidean_distance'].diff()
# put all the euclidean_distance and euclidean_distance_delta into a list as np.array
euclidean_distance_list = []
euclidean_distance_delta_list = []
for i in range(len(df_list)):
    euclidean_distance_list.append(df_list[i]['euclidean_distance'].to_numpy())
    # same but remove first nan value
    euclidean_distance_delta_list.append(df_list[i]['euclidean_distance_delta'].to_numpy()[1:])
# calculate the mean, variance and standard deviation of the euclidean_distance_delta_list
mean_list = []
variance_list = []
standard_deviation_list = []
for i in range(len(df_list)):
    mean_list.append(np.mean(euclidean_distance_delta_list[i]))
    variance_list.append(np.var(euclidean_distance_delta_list[i]))
    standard_deviation_list.append(np.std(euclidean_distance_delta_list[i]))

# #calculate the difference between the x and y columns of the ground truth and the data
for i in range(len(df_list)):
    df_list[i]['x_diff'] = df_list[i]['x'] - df_list[i]['x_gt']
    df_list[i]['y_diff'] = df_list[i]['y'] - df_list[i]['y_gt']
# put all the x_diff and y_diff into a list as np.array
x_diff_list = []
y_diff_list = []
for i in range(len(df_list)):
    x_diff_list.append(df_list[i]['x_diff'].to_numpy())
    y_diff_list.append(df_list[i]['y_diff'].to_numpy())

# check if the first entry of euclidean_distance_delta_list is normally distributed with a shapiro wilk test
print('shapiro wilk test for euclidean_distance_delta_list[0]: ', stats.shapiro(euclidean_distance_delta_list[0]))
# check with kolmogorov smirnov test if the first entry of euclidean_distance_delta_list is normally distributed
print('kolmogorov smirnov test for euclidean_distance_delta_list[0]: ', stats.kstest(euclidean_distance_delta_list[0], 'norm'))
# check with anderson darling test if the first entry of euclidean_distance_delta_list is normally distributed
print('anderson darling test for euclidean_distance_delta_list[0]: ', stats.anderson(euclidean_distance_delta_list[0], 'norm'))
# check with lilliefors test if the first entry of euclidean_distance_delta_list is normally distributed
print('lilliefors test for euclidean_distance_delta_list[0]: ', lilliefors(euclidean_distance_delta_list[0], dist='norm'))

# draw 2000 samples of a normal distrubtion with the same mean and variance as euclidean_distance_delta_list[0]
# plot the samples as histogram together with euclidean_distance_delta_list[0] and with a normal distribution with the same mean and variance
# calc mean and variance of the euclidean_distance_delta_list[0]
mean = np.mean(euclidean_distance_delta_list[0])
variance = np.var(euclidean_distance_delta_list[0])
sigma = np.sqrt(variance)
# draw 2000 samples of a normal distribution with the same mean and variance as euclidean_distance_delta_list[0]
nsize=len(euclidean_distance_delta_list[0])
samples = np.random.normal(mean, sigma, nsize)
# plot the samples as histogram together with euclidean_distance_delta_list[0] and with a normal distribution with the same mean and variance
fig_1, ax = plt.subplots(1, 1)
fig_1.suptitle(suptitle, fontsize=fontsize_title)
ax.yaxis.grid(color='gray', linestyle='dashed')
ax.hist(euclidean_distance_delta_list[0], bins=bins_euclidean_delta, color=color_list[0], label=df_type_name_list[0], alpha=0.5)
hist, bins, _ = ax.hist(samples, bins=bins_euclidean_delta, color=color_list[1], label='samples', alpha=0.5)
# plot them together with one plot command
# ax.hist([euclidean_distance_delta_list[0], samples], bins=bins_euclidean_delta, color=[color_list[0], color_list[1]], label=[df_type_name_list[0], 'samples'], alpha=1.0)
# plot a normal distribution with the same mean and variance
# x = np.linspace(mean - 3*sigma, mean + 3*sigma, 100)
# dont scale it
print(nsize)
p = stats.norm.pdf(bins, mean, sigma)
ax.plot(bins, p/p.sum() * nsize, color=color_list[2], label='normal distribution', alpha=0.5)
ax.legend(loc='upper right', fontsize=fontsize_legend)
ax.set_xlabel('euclidean distance delta [m]', fontsize=fontsize_xlabel)
ax.set_ylabel('count', fontsize=fontsize_ylabel)
ax.tick_params(axis='both', which='major', labelsize=labelsize_axes)
plt.show()
sys.exit()



# plot histo of delta
# fig_2, ax = plt.subplots(1, 1)
# fig_2.suptitle(suptitle, fontsize=fontsize_title)
# ax.yaxis.grid(color='gray', linestyle='dashed')
# ax.hist(euclidean_distance_delta_list[0], bins=bins_euclidean_delta, color=color_list[0], label=df_type_name_list[0], alpha=0.5)
# # get mean and varaice of euclidean_distance_delta_list[0] and plot a normal distribution with the same mean and variance
# mean = np.mean(euclidean_distance_delta_list[0])
# variance = np.var(euclidean_distance_delta_list[0])
# sigma = np.sqrt(variance)
# x = np.linspace(mean - 3*sigma, mean + 3*sigma, 100)
# #scale it such that it fits the histogram
# ax.plot(x, stats.norm.pdf(x, mean, sigma), color=color_list[0], label='normal distribution', linewidth=linewidth_gt)
# ax.set_title('First discrete difference of euclidean distance', fontsize=fontsize_title)
# ax.set_xlabel('first discrete difference', fontsize=fontsize_xlabel)
# ax.set_ylabel('frequency', fontsize=fontsize_ylabel)
# ax.legend(['data', 'est normal'],fontsize=fontsize_legend)
# plt.show()
# sys.exit()
