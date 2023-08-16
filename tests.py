import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from util_hypothesis_tests_2 import *



folders = ["csv/aligned/c8_orb_stereo", "csv/aligned/c8_orb_d435", "csv/aligned/c8_orb_mono"]
columns_ape = [read_cols_from_folder(folder, "ape") for folder in folders]
columns_rpe = [read_cols_from_folder(folder, "rpe") for folder in folders]
# folder_names = folder_names_from_folder_paths(folders)
folder_names = ['stereo', 'RGBD', 'mono']
folder_save = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/results/"
alpha = 0.05
print_every = False
precision = 6
test_names = ["mwu", "ks2"]
num_of_tests_per_slam_combi = len(columns_ape[0])

error_type = "ape"
for error_type in ["ape", "rpe"]:
    if error_type == "ape":
        columns = columns_ape
    else:
        columns = columns_rpe
    for test_idx in range(0, len(test_names)): 
        print("doing test %s error type %s " % (test_names[test_idx], error_type))
        df_diff = pd.DataFrame()
        for i in range(0, len(folders)):
            for j in range(0, i): # begin for loop over slam combinations i!=j
                list_stat_p = hypothesis_test_list(columns[i], columns[j], test_names[test_idx])
                count_fail = sum([1 for i in list_stat_p if i > alpha])
                count_reject = len(list_stat_p) - count_fail
                new_col_name = folder_names[i] + " vs " + folder_names[j]
                df_diff[new_col_name] = list_stat_p + [count_reject, count_fail]
                # end of for loop over slam combinations i!=j

        # name the last two columns reject and fail
        df_diff.rename(index={len(list_stat_p): "reject", len(list_stat_p) + 1: "fail"}, inplace=True)
        # maybe the dataframes need to be split up here vertically if two many combinations are tested. just index the latex tables then with 1,2,3,...
        # make latex string
        latex_string_diff = df_diff.to_latex(header=True, float_format=f"%.{precision}f", index=True)
        # multiline header
        for i in range(0, len(folders)):
            for j in range(0, i):
                new_col_name = folder_names[i] + " vs " + folder_names[j]
                latex_string_diff = latex_string_diff.replace(new_col_name, "\multicolumn{1}{p{2cm}}{\centering %s \\\\  vs  \\\\ %s}" % (folder_names[i], folder_names[j]))
        # line over reject and fail
        latex_string_diff = latex_string_diff.replace('\nreject &', '\n\midrule\nreject &')
        # caption
        latex_string_diff += "\caption{Each column shows the comparison of two \\ac{slam} approaches with %d p-values from \\ac{%s} tests on \\ac{%s} data.}\n" % (num_of_tests_per_slam_combi, test_names[test_idx], error_type)
        # label
        latex_string_diff += "\label{tab:%s_%s}\n" % (error_type, test_names[test_idx])

        # write latex table
        with open(folder_save + error_type + "_" + test_names[test_idx] + ".tex", "w") as f:
            f.write(latex_string_diff)
            f.close()

        # end of loop over tests
        # end of loop over ape rpe



        num_of_tests_per_slam = int(num_of_tests_per_slam_combi/2)
        d = num_of_tests_per_slam

        df_self = pd.DataFrame()
        for i in range(0, len(folders)):
            # begin for loop over slams  i==i
            list_stat_p = hypothesis_test_list(columns[i][:d], columns[i][d:], test_names[test_idx])
            count_fail = sum([1 for i in list_stat_p if i > alpha])
            count_reject = len(list_stat_p) - count_fail
            new_col_name = folder_names[i] + " vs " + folder_names[i]
            df_self[new_col_name] = list_stat_p + [count_reject, count_fail]
            # end of for loop over slam combinations i==i

        # name the last two columns reject and fail
        df_self.rename(index={len(list_stat_p): "reject", len(list_stat_p) + 1: "fail"}, inplace=True)
        # maybe the dataframes need to be split up here vertically if two many combinations are tested. just index the latex tables then with 1,2,3,...
        # make latex string
        latex_string_self = df_self.to_latex(header=True, float_format=f"%.{precision}f", index=True)
        # multiline header
        for i in range(0, len(folders)):
            new_col_name = folder_names[i] + " vs " + folder_names[i]
            latex_string_self = latex_string_self.replace(new_col_name, "\multicolumn{1}{p{2cm}}{\centering %s \\\\  vs  \\\\ %s}" % (folder_names[i], folder_names[i]))
        # line over reject and fail
        latex_string_self = latex_string_self.replace('\nreject &', '\n\midrule\nreject &')
        # caption
        latex_string_self += "\caption{Each column shows the comparison of a \\ac{slam} approach with itself with %d p-values from \\ac{%s} tests on \\ac{%s} data.}\n" % (num_of_tests_per_slam, test_names[test_idx], error_type)
        # label
        latex_string_self += "\label{tab:%s_%s_self}\n" % (error_type, test_names[test_idx])

        # write latex table
        with open(folder_save + error_type + "_" + test_names[test_idx] + "_self.tex", "w") as f:
            f.write(latex_string_self)
            f.close()