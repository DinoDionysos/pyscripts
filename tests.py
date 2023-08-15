import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from util_hypothesis_tests_2 import *



folders = ["csv/aligned/c8_orb_stereo", "csv/aligned/c8_orb_d435"]
columns_ape = [read_cols_from_folder(folder, "ape") for folder in folders]
columns_rpe = [read_cols_from_folder(folder, "rpe") for folder in folders]
folder_names = folder_names_from_folder_paths(folders)
folder_save = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/results/"
alpha = 0.05
print_every = False
precision = 4
test_names = ["mwu", "ks2"]
num_of_tests_per_slam_combi = len(columns_ape[0])

error_type = "ape" #begin loop over ape rpe

test_idx = 1 #begin for loop over tests

i = 0
j = 1 # begin for loop over slam combinations i!=j

df = pd.DataFrame()
# test columns ape 1 and 2 with an mwu test with hypothesis_test_list
list_stat_p = hypothesis_test_list(columns_ape[i], columns_ape[j], test_names[test_idx])
count_fail = sum([1 for i in list_stat_p if i < alpha])
count_reject = len(list_stat_p) - count_fail
new_col_name = folder_names[i] + " vs " + folder_names[j]
df[new_col_name] = list_stat_p + [count_reject, count_fail]
# end of for loop over slam combinations i!=j

# name the last two columns reject and fail
df.rename(index={len(list_stat_p): "reject", len(list_stat_p) + 1: "fail"}, inplace=True)
# maybe the dataframes need to be split up here vertically if two many combinations are tested. just index the latex tables then with 1,2,3,...
# make latex string
latex_string = df.to_latex(header=True, float_format=f"%.{precision}f", index=True)
# multiline header
new_col_name = folder_names[i] + " vs " + folder_names[j]
latex_string = latex_string.replace(new_col_name, "\multicolumn{1}{p{2cm}}{\centering %s \\\\  vs  \\\\ %s}" % (folder_names[i], folder_names[j]))
# line over reject and fail
latex_string = latex_string.replace('\nrejected &', '\n\midrule\nrejected &')
# caption
latex_string += "\caption{Each column shows the comparison of two \\ac{slam} approaches with %d p-values of \\ac{%s} tests on \\ac{%s} data.}\n" % (num_of_tests_per_slam_combi, test_names[test_idx], error_type)
# label
latex_string += "\label{tab:%s_%s}\n" % (error_type, test_names[test_idx])

# write latex table
with open(folder_save + error_type + "_" + test_names[test_idx] + ".tex", "w") as f:
    f.write(latex_string)
    f.close()

# end of loop over tests
# end of loop over ape rpe