import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from util_hypothesis_tests_2 import hypothesis_test_list
from util_hypothesis_tests_2 import read_cols_from_folder
from util_hypothesis_tests_2 import correlation_value_list
from util_hypothesis_tests_2 import normal_test_list


from util_latex_tables import *
from util_latex_tables_2 import *
from util_error_measures import *


scenario_names = {
    9: "wide outdoor loop",
    15: "narrow outdoor space",
    28: "collapsed fire station",
    19: "wide outdoor straight",
    17: "narrow outdoor straight",
    51: "collapsed house indoor",
    49: "wide outdoor curvy",
    34: "narrow outdoor curvy"
}

save_flag = True

scenarios_num = [9, 15, 28, 19, 17, 51, 49, 34]
# scenarios_num = [15, 28, 19, 17, 51, 49, 34]
scenarios = ["c"+str(i) for i in scenarios_num]
from util import type_yes_to_save
if save_flag:
    print("########## SECOND TEST SECOND TEST SECOND TEST #############")
    save_flag = type_yes_to_save(save_flag, scenarios)
else:
    print("No plots and tables will be saved.")
    sys.exit(1)

c=-1
for scenario in scenarios:
    c+=1
    folder_latex_inputs_fig_caption_labels = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/inputs/input_results/fig_captions_labels/" + scenario + "/"
    if not os.path.exists(folder_latex_inputs_fig_caption_labels):
        os.makedirs(folder_latex_inputs_fig_caption_labels)
    
    print('scenario', scenario)
    folder_results_win = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/results/"
    folder_results_ssd = "/mnt/d/results/"
    folder_save = folder_results_win + scenario + "/tables_compact/"
    if not os.path.exists(folder_save):
        os.makedirs(folder_save)

    folder_ssd = "/mnt/d/"
    slam_names_for_files = ["stereo", "d435", "mono"]
    temp = folder_ssd+"csv/orb/aligned/"+scenario+"_orb_"
    folders = [temp + slam_names_for_files[i] for i in range(0, len(slam_names_for_files))]

    list_xy_yaw_rpe_ape_combis = ["xy_ape", "xy_rpe", "yaw_ape", "yaw_rpe"]
    # 0: xy_ape, 
    # 1: xy_rpe, 
    # 2: yaw_ape, 
    # 3: yaw_rpe
    xy_yaw_rpe_ape_columns = [[read_cols_from_folder(folder, xy_yaw_rpe_ape) for folder in folders] for xy_yaw_rpe_ape in list_xy_yaw_rpe_ape_combis]

    names_of_slams = ['ORB-SLAM stereo', 'ORB-SLAM RGBD', 'ORB-SLAM mono']
    short_of_slams = ['stereo', 'RGBD', 'mono']
    alpha = 0.05
    precision = 2
    test_names = ["KS2", "TAU"]#, "TAU"]
    test_names_normal = ["SW", "KS", "SK", "LF"]
    correlation_names = []#"f"]

    ################################# loop slam combis ###########################
    for slam_idx_1 in range(0,len(folders)):
        for slam_idx_2 in range(0, slam_idx_1):
            df = pd.DataFrame()
            # make the Dataframe the correct form and fill it
            #TODO: add test_names to the function parameters
            df = df_latex_table_template(test_names, correlation_names)
            df = insert_multicol_at(df, 'Scenario '+scenario_names[scenarios_num[c]]+':', 0)
            df = insert_multicol_at(df,names_of_slams[slam_idx_1]+' and '+ names_of_slams[slam_idx_2], 1)
            df = insert_multicol_at(df, 'Significance level $\\alpha$ = '+str(alpha)+", 20 repetitions", 2)
            # print('hello from slam', slam_idx_1, slam_idx_2)
            ############################### loop rotat trans ####################
            data_idx = -1
            for data_type in ["xy", "yaw"]:
                data_idx += 1
                if data_type == "xy":
                    data_type_print = "translational"
                else:
                    data_type_print = "rotational"
                
                ############################### loop error ape rpe ################
                error_idx = -1
                for error_type in ["ape", "rpe"]:
                    # print('error type is here', error_type)
                    error_idx += 1
                    columns = xy_yaw_rpe_ape_columns[2*data_idx+error_idx]
                    ############################### loop tests ####################
                    offset_row = 6
                    offset_col = 3
                    for test_idx in range(0, len(test_names)): 
                        # print('test_idx', test_idx)
                        list_pvalues = hypothesis_test_list(
                            columns[slam_idx_1], 
                            columns[slam_idx_2], 
                            test_name = test_names[test_idx])
                        # count the number of pvalues that are above alpha
                        count_fail = sum([1 for i in list_pvalues if i > alpha])
                        # count the number of pvalues that are below alpha
                        count_reject = len(list_pvalues) - count_fail
                        # use insert_line_at and insert_at to fill the dataframe
                        row_index=offset_row+data_idx*6+3*error_idx
                        col_idx=offset_col+test_idx
                        df.iloc[row_index, col_idx] = count_reject
                        df.iloc[row_index+1, col_idx] = count_fail
                    ############################### loop correlation ##########
                    for correlation_idx in range(0, len(correlation_names)):
                        # print('correlation_idx', correlation_idx)
                        # here we have a combination of two slams and their index
                        # and now we loop every test to do the N correlation coefficients and a column in the dataframe
                        list_correlation_values = correlation_value_list(
                            columns[slam_idx_1], 
                            columns[slam_idx_2], 
                            correlation_name = correlation_names[correlation_idx])
                        # mean of list_correlation_values
                        mean = np.mean(np.array(list_correlation_values))
                        std = np.std(np.array(list_correlation_values))
                        row_index=offset_row+data_idx*6+3*error_idx
                        col_idx=offset_col+len(test_names)+1+correlation_idx
                        df.iloc[row_index, col_idx] = mean
                        df.iloc[row_index+1, col_idx] = std
            caption = "Scenario %s: Evaluation of %s and %s. The table shows the counts of rejections and fails of rejection of 20 repetitions of the hypothesis tests \\ac{ks2} and Kendall's Tau with significance level 0.05. The tests were applied on the translational \\ac{ape} and \\ac{rpe} as well as the rotational." % (
                            scenario_names[scenarios_num[c]],
                            short_of_slams[slam_idx_1], 
                            short_of_slams[slam_idx_2])
            label = "tab:compact_%s_%s_%s" % (
                scenario,
                short_of_slams[slam_idx_1], 
                short_of_slams[slam_idx_2])
            # save the label and caption in a file in folder_latex_inputs_fig_caption_labels
            if save_flag:
                save_latex_table(
                    add_caption_label_to_latex_string("", caption, label), 
                    folder_latex_inputs_fig_caption_labels, 
                    scenario+"_"+short_of_slams[slam_idx_1]+"_"+short_of_slams[slam_idx_2]+"_compact.tex")
            # def to latex with function from util_latex_tables_2.py
            latex_string_table = latex_table_from_df_template(df, precision, test_names, correlation_names)
            save_name = "compact_"+\
                short_of_slams[slam_idx_1] +"_"+ \
                short_of_slams[slam_idx_2] + ".tex"
            if save_flag:
                save_latex_table(
                    latex_string_table, 
                    folder_save, 
                    save_name)
                    
                    
                









                    
                    
