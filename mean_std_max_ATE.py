import os
import numpy as np

from util_hypothesis_tests_2 import read_cols_from_folder
from util_error_measures import *
from util_latex_tables import *

# for changing to another simulation scenario the following variables need to be changed:
scenario = "c34"
folder_results_win = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/results/"
folder_results_ssd = "/mnt/d/results/"
folder_save = folder_results_win + scenario + "/tables_ate_rte/"
if not os.path.exists(folder_save):
    os.makedirs(folder_save)

folder_ssd = "/mnt/d/"
slam_names_for_files = ["stereo", "d435", "mono"]
temp = folder_ssd+"csv/orb/aligned/"+scenario+"_orb_"
folders = [temp + slam_names_for_files[i] for i in range(0, len(slam_names_for_files))]

names_of_slams = ['ORB-SLAM stereo', 'ORB-SLAM RGBD', 'ORB-SLAM mono']
short_of_slams = ['stereo', 'RGBD', 'mono']
           
list_slam_repet_trajec_ape = [read_cols_from_folder(folder, "xy_ape") for folder in folders] 
# list of length #folders of lists of length N with array with #(poses in traj) ape elements
# N ape arrays pro SLAM
list_slam_repet_trajec_rpe = [read_cols_from_folder(folder, "xy_rpe") for folder in folders]


for indexx in range(0,2):
    if indexx == 0:
        list_slam_repet_trajec_ape = [read_cols_from_folder(folder, "xy_ape") for folder in folders] 
        list_slam_repet_trajec_rpe = [read_cols_from_folder(folder, "xy_rpe") for folder in folders]
        data_type = "xy"
    else:
        list_slam_repet_trajec_ape = [read_cols_from_folder(folder, "yaw_ape") for folder in folders] 
        list_slam_repet_trajec_rpe = [read_cols_from_folder(folder, "yaw_rpe") for folder in folders]
        data_type = "yaw"


    # list length #slams with arrays length N with T ate elements
    # N ates pro SLAM
    list_slam_repet_ate = [ates_from_columns(list_slam_repet_trajec_ape[i]) for i in range(0, len(list_slam_repet_trajec_ape))]
    # make mean and std of ate. list of length #slams
    # ATE mean über alle N Trajektorien
    list_slam_ate_mean = [np.mean(list_slam_repet_ate[i]) for i in range(0, len(list_slam_repet_ate))]
    # ATE std über alle N Trajektorien
    list_slam_ate_std = [np.std(list_slam_repet_ate[i]) for i in range(0, len(list_slam_repet_ate))]
    # ATE max über alle N Trajektorien
    list_slam_ate_max = [np.max(list_slam_repet_ate[i]) for i in range(0, len(list_slam_repet_ate))]
    #gesamte std über alle ape aus alle trajectorien zusammen genommen

    # make dataframe from list_slam_ate_mean
    df_ate = pd.DataFrame()
    df_ate["mean"] = list_slam_ate_mean
    df_ate["std"] = list_slam_ate_std
    df_ate["max"] = list_slam_ate_max
    # to latex
    latex_ate = df_ate.to_latex()
    for i in range(0, len(short_of_slams)):
        latex_ate = latex_ate.replace('\n'+str(i)+' & ', '\n'+short_of_slams[i]+' & ')
    # replace "\toprule \\ & mean" with "\toprule \\ ATE (mm) & mean"
    latex_ate = latex_ate.replace(' & mean', 'ATE (mm) & mean')
    save_latex_table(latex_ate, folder_save, data_type+"_ate_mean_std_max.tex")
    print(latex_ate)

    list_slam_repet_rte = [ates_from_columns(list_slam_repet_trajec_rpe[i]) for i in range(0, len(list_slam_repet_trajec_rpe))]
    # make mean, std and max of rte
    list_slam_rpe_mean = [np.mean(list_slam_repet_rte[i]) for i in range(0, len(list_slam_repet_rte))]
    list_slam_rpe_std = [np.std(list_slam_repet_rte[i]) for i in range(0, len(list_slam_repet_rte))]
    list_slam_rpe_max = [np.max(list_slam_repet_rte[i]) for i in range(0, len(list_slam_repet_rte))]

    # make dataframe from list_slam_rpe_mean
    df_rpe = pd.DataFrame()
    df_rpe["mean"] = list_slam_rpe_mean
    df_rpe["std"] = list_slam_rpe_std
    df_rpe["max"] = list_slam_rpe_max
    # to latex
    latex_rpe = df_rpe.to_latex()
    for i in range(0, len(short_of_slams)):
        latex_rpe = latex_rpe.replace('\n'+str(i)+' & ', '\n'+short_of_slams[i]+' & ')
    latex_rpe = latex_rpe.replace(' & mean', 'RTE (mm) & mean')
    save_latex_table(latex_rpe, folder_save, data_type+"_rpe_mean_std_max.tex")
    print(latex_rpe)



