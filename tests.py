import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from util_hypothesis_tests_2 import hypothesis_test_list
from util_hypothesis_tests_2 import read_cols_from_folder
from util_latex_tables import *
from util_error_measures import *



folders = ["csv/aligned/c8_orb_stereo", "csv/aligned/c8_orb_d435", "csv/aligned/c8_orb_mono"]
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

# list length #slams with arrays length N with ate elements
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
for i in range(0, len(names_of_slams)):
    latex_ate = latex_ate.replace('\n'+str(i)+' & ', '\n'+names_of_slams[i]+' & ')
# replace "\toprule \\ & mean" with "\toprule \\ ATE (mm) & mean"
latex_ate = latex_ate.replace(' & mean', 'ATE (mm) & mean')
save_latex_table(latex_ate, folder_save, "ate", "mean_std_max")
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
for i in range(0, len(names_of_slams)):
    latex_rpe = latex_rpe.replace('\n'+str(i)+' & ', '\n'+names_of_slams[i]+' & ')
latex_rpe = latex_rpe.replace(' & mean', 'RTE (mm) & mean')
save_latex_table(latex_rpe, folder_save, "rpe", "mean_std_max")
print(latex_rpe)







for error_type in ["ape", "rpe"]:
    if error_type == "ape":
        columns = list_slam_repet_trajec_ape
    else:
        columns = list_slam_repet_trajec_rpe
    for test_idx in range(0, len(test_names)): 
        print("doing test %s error type %s " % (test_names[test_idx], error_type))

        ### make dataframe and calculations ####################################
        df_diff = pd.DataFrame()
        for i in range(0, len(folders)):
            for j in range(0, i): # begin for loop over slam combinations i!=j
                list_pvalues = hypothesis_test_list(columns[i], columns[j], test_names[test_idx])
                count_fail = sum([1 for i in list_pvalues if i > alpha])
                count_reject = len(list_pvalues) - count_fail
                # new_col_name = names_for_headers[i] + " vs " + names_for_headers[j]
                new_col_name = make_column_header(names_of_slams[i], names_of_slams[j])
                df_diff[new_col_name] = list_pvalues + [count_reject, count_fail]
                # end of for loop over slam combinations i!=j
        # name the last two columns reject and fail
        df_diff.rename(index={len(list_pvalues): "reject", len(list_pvalues) + 1: "fail"}, inplace=True)
        ## end make dataframe and caluclations #################################

        # maybe the dataframes need to be split up here vertically if two many combinations are tested. just index the latex tables then with 1,2,3,...
        postfix = "to_another"
        caption = "\caption{Each column shows the comparison of two \\ac{slam} approaches with %d p-values from \\ac{%s} tests on \\ac{%s} data.}\n" % (num_of_tests_per_slam_combi, test_names[test_idx], error_type)
        label = "\label{tab:%s_%s_%s}\n" % (test_names[test_idx], error_type, postfix)
        ## make latex string
        latex_string_diff = make_latex_table_pvalues_reject_fail(df_diff, caption, label, precision)
        # write latex table
        save_latex_table(latex_string_diff, folder_save, error_type, test_names[test_idx], postfix)

        # end of loop over tests
        # end of loop over ape rpe



        num_of_tests_per_slam = int(num_of_tests_per_slam_combi/2)
        d = num_of_tests_per_slam

        df_self = pd.DataFrame()
        for i in range(0, len(folders)):
            # begin for loop over slams  i==i
            list_pvalues = hypothesis_test_list(columns[i][:d], columns[i][d:], test_names[test_idx])
            count_fail = sum([1 for i in list_pvalues if i > alpha])
            count_reject = len(list_pvalues) - count_fail
            new_col_name = make_column_header(names_of_slams[i], names_of_slams[j])
            df_self[new_col_name] = list_pvalues + [count_reject, count_fail]
            # end of for loop over slam combinations i==i
        # name the last two columns reject and fail
        df_self.rename(index={len(list_pvalues): "reject", len(list_pvalues) + 1: "fail"}, inplace=True)

        # maybe the dataframes need to be split up here vertically if two many combinations are tested. just index the latex tables then with 1,2,3,...
        postfix = "to_itself"
        caption = "\caption{Each column shows the comparison of a \\ac{slam} approach with itself with %d p-values from \\ac{%s} tests on \\ac{%s} data.}\n" % (num_of_tests_per_slam, test_names[test_idx], error_type)
        label = "\label{tab:%s_%s_%s}\n" % (test_names[test_idx], error_type, postfix)
        # make latex string
        latex_string_self = make_latex_table_pvalues_reject_fail(df_self, caption, label, precision)

        # write latex table
        save_latex_table(latex_string_self, folder_save, error_type, test_names[test_idx], postfix)