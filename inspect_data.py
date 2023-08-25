
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from util_error_measures import *

folders = ["csv/aligned/c8_orb_stereo", "csv/aligned/c8_orb_d435", "csv/aligned/c8_orb_mono"]
folder_save = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/results/"
# list of length #folders of lists of length N with array with #(poses in traj) ape elements
list_slam_repet_trajec_ape = [read_cols_from_folder(folder, "ape") for folder in folders] 
names_of_slams = ['dataset 1', 'dataset 2', 'mono']


#concatente all ape arrays to one big ape array
list_slam_concat_ape = []
for i in range(0, len(list_slam_repet_trajec_ape)):
    #concat the ape arrays of the different trajectories in list_slam_repet_trajec_ape[i]
    list_slam_concat_ape.append(np.concatenate(list_slam_repet_trajec_ape[i]))
    print(np.shape(list_slam_concat_ape[i]))

for i in range(0, 2):#len(list_slam_concat_ape)):
    N = len(list_slam_concat_ape[i])
    x = np.sort(list_slam_concat_ape[i])
    
    # get the cdf values of y
    y = np.arange(N) / float(N)
    #plot
    plt.plot(x, y, label = names_of_slams[i])
plt
plt.xlabel('APE (mm)')
plt.ylabel('Cumulative Probability')
plt.legend()
plt.title('Two Empirical Cumulative Distribution Functions')
# save plot as pdf in folder save
plt.savefig(os.path.join(folder_save, 'ape_cdf.pdf'), bbox_inches='tight')
# save as png too
plt.savefig(os.path.join(folder_save, 'ape_cdf.png'), bbox_inches='tight')
plt.show()




# get the std deviation of the concatenated ape arrays
list_slam_std_ape = [np.std(list_slam_concat_ape[i]) for i in range(0, len(list_slam_concat_ape))]
print("list_slam_std_ape: ", list_slam_std_ape)
# get the mean
list_slam_mean_ape = [np.mean(list_slam_concat_ape[i]) for i in range(0, len(list_slam_concat_ape))]
print("list_slam_mean_ape: ", list_slam_mean_ape)






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





