import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from util_hypothesis_tests_2 import hypothesis_test_list
from util_hypothesis_tests_2 import read_cols_from_folder
from util_latex_tables import *
from util_error_measures import *

# for changing to another simulation scenario the following variables need to be changed:
scenario = "c8"

folders = ["csv/aligned/"+scenario+"_orb_stereo",\
            "csv/aligned/"+scenario+"_orb_d435",\
            "csv/aligned/"+scenario+"_orb_mono"]
list_slam_repet_trajec_ape = [read_cols_from_folder(folder, "ape") for folder in folders] 
# list of length #folders of lists of length N with array with #(poses in traj) ape elements
# N ape arrays pro SLAM
list_slam_repet_trajec_rpe = [read_cols_from_folder(folder, "rpe") for folder in folders]
# folder_names = folder_names_from_folder_paths(folders)
names_of_slams = ['stereo', 'RGBD', 'mono']
folder_save = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/results/"
alpha = 0.05
print_every = False
precision = 6
test_names = ["mwu", "ks2"]
num_of_tests_per_slam_combi = len(list_slam_repet_trajec_ape[0])




fontsize = 15


def make_cdf(data):
    "np.array with the apes or rpes. return sorted array and cdf values to plot"
    N = len(data)
    x = np.sort(data)
    # get the cdf values of y
    y = np.arange(N) / float(N)
    return x, y
#make list of twenty different colors
colors = plt.cm.tab20(np.linspace(0,1,20))
#make 3 line styles
line_styles = ['-', '--', ':']
color_slams = [colors[0], 'black', 'red']
linewidth = [1, 1, 1.5]
list_slam_concat_ape = []
for i in range(0, len(list_slam_repet_trajec_ape)):
    #concat the ape arrays of the different trajectories in list_slam_repet_trajec_ape[i]
    list_slam_concat_ape.append(np.concatenate(list_slam_repet_trajec_ape[i]))
    print(np.shape(list_slam_concat_ape[i]))

for error_type in ["ape"]:#, "rpe"]:
    if error_type == "ape":
        columns = list_slam_repet_trajec_ape
    else:
        columns = list_slam_repet_trajec_rpe
    # iterate over all trajectories
    for j in range(0, len(columns[i])):
        # iterate over all slams
        for i in range(0, len(folders)):
            # make cdf
            x, y = make_cdf(columns[i][j])
            # plot
            plt.plot(x, y, color=color_slams[i], linestyle=line_styles[i], alpha=1.0, linewidth=linewidth[i])
        # end for loop over slams   
    # end for loop over trajectories
    plt.xlabel(error_type.upper() + " (mm)")
    plt.ylabel('Cumulative Probability')
    # plt.legend()
    plt.title('Empirical Cumulative Distribution Functions')

# for i in range(0, len(list_slam_concat_ape)):
#     # make cdf
#     x, y = make_cdf(list_slam_concat_ape[i])
#     # plot
#     plt.plot(x, y, color=color_slams[i], linestyle=line_styles[i], linewidth=6, alpha = 0.5, label=names_of_slams[i])
#legende in lower right corner
plt.legend(names_of_slams, loc='lower right', fontsize=fontsize)
# save plot as pdf in folder save
plt.savefig(os.path.join(folder_save, error_type + '_cdfs.pdf'), bbox_inches='tight')
plt.show()
sys.exit(1)