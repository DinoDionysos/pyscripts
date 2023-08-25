
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from util_error_measures import *

folders = ["csv/aligned/c8_orb_stereo", "csv/aligned/c8_orb_d435", "csv/aligned/c8_orb_mono"]
folder_save = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/results/"
# list of length #folders of lists of length N with array with #(poses in traj) ape elements
list_slam_repet_trajec_ape = [read_cols_from_folder(folder, "ape") for folder in folders] 
names_of_slams = ['stereo', 'RGBD', 'mono']


#concatente all ape arrays to one big ape array
list_slam_concat_ape = []
for i in range(0, len(list_slam_repet_trajec_ape)):
    #concat the ape arrays of the different trajectories in list_slam_repet_trajec_ape[i]
    list_slam_concat_ape.append(np.concatenate(list_slam_repet_trajec_ape[i]))
    print(np.shape(list_slam_concat_ape[i]))

# do the stuff above again but use a different name for the k variable each
# time so that we can plot all the histograms in one plot
#sturge's rule: k = 1 + 3.322 * log(N)
N = len(list_slam_concat_ape[0])
k_sturges = 1 + 3.322 * np.log(N)
k_sturges = int(k_sturges)
print("sturges k: ", k_sturges)
#doane's rule: k = 1 + log(N) + log(1 + |g1|/sigma_g1)
#import skewness and kurtosis from scipy.stats
from scipy.stats import skew, kurtosis
g1 = skew(list_slam_concat_ape[0])
sigma_g1 = np.sqrt(kurtosis(list_slam_concat_ape[0]))
k_doanes = 1 + np.log(N) + np.log(1 + np.abs(g1)/sigma_g1)
# k_doanes = int(k_doanes)
print("doanes k: ", k_doanes)
k_doanes = 3
#scott's rule: k = 3.5 * sigma / N^(1/3)
sigma = np.std(list_slam_concat_ape[0])
k_scott = 3.5 * sigma / N**(1/3)
k_scott = int(k_scott)
print("scott's k: ", k_scott)
#rice rule: k = 2 * N^(1/3)
k_rice = 2 * N**(1/3)
k_rice = int(k_rice)
print("rice k: ", k_rice)
#freedman-diaconis rule: k = 2 * IQR / N^(1/3)
from scipy.stats import iqr
IQR = iqr(list_slam_concat_ape[0])
k_freedman = 2 * IQR / N**(1/3)
k_freedman = int(k_freedman)
print("freedman-diaconis k: ", k_freedman)
#square-root rule: k = sqrt(N)
k_sqrt = np.sqrt(N)
k_sqrt = int(k_sqrt)
print("square-root k: ", k_sqrt)
#sturges rule: k = log2(N) + 1
k_log2 = np.log2(N) + 1
k_log2 = int(k_log2)
print("log2 k: ", k_log2)

# make k_list
k_list = [k_log2, 20, k_sturges, 40, 50, k_rice, 100,k_sqrt]
# rice and sturges seem good
# rice is enough for the effects

# for every k do a histogram in a subplot
fig, axs = plt.subplots(2, 4)
fig.suptitle('Histograms of APE')
for i in range(0, len(k_list)):
    # print("i: ", i)
    # print("k_list[i]: ", k_list[i])
    # print("axs[i//4, i%4]: ", axs[i//4, i%4])
    axs[i//4, i%4].hist(list_slam_concat_ape[0], bins = k_list[i], density=True, histtype='stepfilled', label=names_of_slams[0], linewidth=2, alpha=1.0, color=np.array([0.2, 0.2, 0.2, 1.0]))
    axs[i//4, i%4].hist(list_slam_concat_ape[1], bins = k_list[i], density=True, histtype='stepfilled', label=names_of_slams[1], linewidth=2, alpha=0.5, color='green', edgecolor='darkgreen')
    axs[i//4, i%4].hist(list_slam_concat_ape[1], bins = k_list[i], density=True, histtype='step', linewidth=2, alpha=1.0, color='green', edgecolor='darkgreen')
    axs[i//4, i%4].hist(list_slam_concat_ape[2], bins = k_list[i], density=True, histtype='step', label=names_of_slams[2], linewidth=1.5, alpha=1.0, color='red')
    axs[i//4, i%4].set_title('k = ' + str(k_list[i]))
    axs[i//4, i%4].set_xlabel('APE (mm)')
    axs[i//4, i%4].set_ylabel('Frequency')
    axs[i//4, i%4].legend()
    #scale y axis to 0.0 to 1.0
    axs[i//4, i%4].set_ylim(0.0, 0.007)
plt.show()



plt.hist(list_slam_concat_ape, bins = 160, density=True, histtype='step', label=names_of_slams)
plt.xlabel('APE (mm)')
plt.ylabel('Frequency')
plt.title('Histogram of APE')
plt.legend(names_of_slams)
plt.show()


# for i in range(0, 2):#len(list_slam_concat_ape)):
#     N = len(list_slam_concat_ape[i])
#     x = np.sort(list_slam_concat_ape[i])
    
#     # get the cdf values of y
#     y = np.arange(N) / float(N)
#     #plot
#     plt.plot(x, y, label = names_of_slams[i])
# plt
# plt.xlabel('APE (mm)')
# plt.ylabel('Cumulative Probability')
# plt.legend()
# plt.title('Two Empirical Cumulative Distribution Functions')
# # save plot as pdf in folder save
# plt.savefig(os.path.join(folder_save, 'ape_cdf.pdf'), bbox_inches='tight')
# # save as png too
# plt.savefig(os.path.join(folder_save, 'ape_cdf.png'), bbox_inches='tight')
# plt.show()



# # get the std deviation of the concatenated ape arrays
# list_slam_std_ape = [np.std(list_slam_concat_ape[i]) for i in range(0, len(list_slam_concat_ape))]
# print("list_slam_std_ape: ", list_slam_std_ape)
# # get the mean
# list_slam_mean_ape = [np.mean(list_slam_concat_ape[i]) for i in range(0, len(list_slam_concat_ape))]
# print("list_slam_mean_ape: ", list_slam_mean_ape)

#plot them as bar plot
# plt.bar(names_of_slams, list_slam_mean_ape, yerr=list_slam_std_ape)
# plt.ylabel('APE (mm)')
# plt.title('Mean and Standard Deviation of APE')
# plt.show()











# list_slam_repet_trajec_rpe = [read_cols_from_folder(folder, "rpe") for folder in folders]
# # concatente all rpe arrays to one big rpe array
# list_slam_concat_rpe = []
# for i in range(0, len(list_slam_repet_trajec_rpe)):
#     #concat the ape arrays of the different trajectories in list_slam_repet_trajec_ape[i]
#     list_slam_concat_rpe.append(np.concatenate(list_slam_repet_trajec_rpe[i]))
#     print(np.shape(list_slam_concat_rpe[i]))

# for i in range(0, len(list_slam_concat_rpe)):
#     N = len(list_slam_concat_rpe[i])
#     x = np.sort(list_slam_concat_rpe[i])
    
#     # get the cdf values of y
#     y = np.arange(N) / float(N)
#     #plot
#     plt.plot(x, y, label = names_of_slams[i])
# plt.xlabel('RPE (mm)')
# plt.ylabel('CDF')
# plt.legend()
# plt.show()





