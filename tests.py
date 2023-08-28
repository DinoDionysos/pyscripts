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
from util_error_measures import *

# for changing to another simulation scenario the following variables need to be changed:
scenario = "c8"
folder_save = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/results/tables/"
if not os.path.exists(folder_save):
    os.makedirs(folder_save)

folders = ["csv/aligned/"+scenario+"_orb_stereo",\
            "csv/aligned/"+scenario+"_orb_d435",\
            "csv/aligned/"+scenario+"_orb_mono"]
list_slam_repet_trajec_ape = [read_cols_from_folder(folder, "xy_ape") for folder in folders] 
# list of length #folders of lists of length N with array with #(poses in traj) ape elements
# N ape arrays pro SLAM
list_slam_repet_trajec_rpe = [read_cols_from_folder(folder, "xy_rpe") for folder in folders]
# folder_names = folder_names_from_folder_paths(folders)
names_of_slams = ['ORB-SLAM stereo', 'ORB-SLAM RGBD', 'ORB-SLAM mono']
short_of_slams = ['stereo', 'RGBD', 'mono']
alpha = 0.05
print_every = False
precision = 4
test_names = ["KS2", 'BF', "KW", 'BM', "MWU"]
test_names_normal = ["SW", "KS", "SK", "LF"]
correlation_names = ["f", "r"]
num_of_tests_per_slam_combi = len(list_slam_repet_trajec_ape[0])






#hierarchy of the datastructures:
# level 1: slam
# level 2: repetition of trajectory on same rosbag
# level 3: poses in the trajectory

# makes 4 tables (to another)
# every table has every slam combination
# with 20 hypothesis tests

for error_type in ["ape", "rpe"]:
    for data_type in ["xy", "yaw"]:
        columns = [read_cols_from_folder(folder, data_type+'_'+error_type) for folder in folders]
        if data_type == "xy":
            data_type_print = "translational"
        else:
            data_type_print = "rotational"
        for verbose_table in [True, False]:
            if verbose_table:
                verbose_string = "_verbose"
                subfolder_save = "verbose/"
                if not os.path.exists(folder_save + subfolder_save):
                    os.makedirs(folder_save + subfolder_save)
            else:
                verbose_string = ""
                subfolder_save = ""
            for slam_idx_1 in range(0,len(folders)):
                for slam_idx_2 in range(0, slam_idx_1):
                    # here we have a combination of two slams and their index
                    # and now we loop every test to do the N tests and a column in the dataframe
                    df = pd.DataFrame()
                    for test_idx in range(0, len(test_names)): 
                        # here we have a combination of two slams and their index
                        # and now we loop every test to do the N tests and a column in the dataframe
                        list_pvalues = hypothesis_test_list(columns[slam_idx_1], columns[slam_idx_2], test_name = test_names[test_idx])
                        # count the number of pvalues that are above alpha
                        count_fail = sum([1 for i in list_pvalues if i > alpha])
                        # count the number of pvalues that are below alpha
                        count_reject = len(list_pvalues) - count_fail
                        # make a new column name
                        new_col_name = test_names[test_idx]
                        # put the list of pvalues and the counts in the dataframe
                        if verbose_table:
                            df[new_col_name] = list_pvalues + [count_reject, count_fail]
                        else:
                            df[new_col_name] = [count_reject, count_fail]
                        # end of loop over test
                    # name the last two columns reject and fail
                    #get the length of the dataframe
                    df.rename(index={len(df)-2: "reject", len(df)-1: "fail"}, inplace=True)
                    mean_to_replace = 0
                    std_to_replace = 0
                    mean_to_replace_2 = 0
                    std_to_replace_2 = 0
                    for correlation_idx in range(0, len(correlation_names)):
                        # here we have a combination of two slams and their index
                        # and now we loop every test to do the N correlation coefficients and a column in the dataframe
                        list_correlation_values = correlation_value_list(
                            columns[slam_idx_1], 
                            columns[slam_idx_2], 
                            correlation_name = correlation_names[correlation_idx])
                        # mean of list_correlation_values
                        mean = np.mean(np.array(list_correlation_values))
                        std = np.std(np.array(list_correlation_values))
                        if correlation_idx == 0:
                            mean_to_replace = mean
                            std_to_replace = std
                        if correlation_idx == 1:
                            mean_to_replace_2 = mean
                            std_to_replace_2 = std
                        # make a new column name
                        new_col_name = correlation_names[correlation_idx]
                        # put the list of correlation 
                        if verbose_table:
                            df[new_col_name] = list_correlation_values + [mean,std]
                        else:
                            df[new_col_name] = [mean,std]
                        # end of loop over test
                    # maybe the dataframes need to be split up here vertically if two many combinations are tested. just index the latex tables then with 1,2,3,...
                    postfix = ""
                    if verbose_table:
                        verbose_switch_1 = "A column shows the p-values of a hypothesis tests on 20 trajectory pairs. The bottom two rows "
                        verbose_switch_2 = "effect strength coefficients $f$ and $r$. Their means and standard deviations are in the bottom two rows"
                    else:
                        verbose_switch_1 = "The table shows"
                        verbose_switch_2 = "means and standard deviations of the effect strength coefficients $f$ and $r$"
                    caption = "\caption{Comparison of %s and %s. %s the counts of rejection and fails of rejection. The two columns on the right show the %s. The error measure is the %s \\ac{%s}.}\n" % (
                        names_of_slams[slam_idx_1], 
                        names_of_slams[slam_idx_2],
                        verbose_switch_1,
                        verbose_switch_2,
                        data_type_print, 
                        error_type)
                    label = "\label{tab:%s_%s_%s_%s_%s}\n" % (
                        names_of_slams[slam_idx_1], 
                        names_of_slams[slam_idx_2],
                        data_type, 
                        error_type, 
                        postfix)
                    title = "& & \multicolumn{%d}{c}{%s and %s | error = %s \\ac{%s}} & \\\\ \n \midrule"%(
                        len(test_names), 
                        names_of_slams[slam_idx_1], 
                        names_of_slams[slam_idx_2], 
                        data_type_print, error_type)
                    title = "\multicolumn{%d}{c}{%s and %s}\\\\ \multicolumn{%d}{c}{error = %s \\ac{%s}}\\\\ \multicolumn{%d}{c}{significance level $\\alpha$ = %d%s}\\\\"%(
                        len(test_names)+len(correlation_names)+1,
                        names_of_slams[slam_idx_1], 
                        names_of_slams[slam_idx_2], 
                        len(test_names)+len(correlation_names)+1,
                        data_type_print, 
                        error_type,
                        len(test_names)+len(correlation_names)+1,
                        alpha*100, "\%")
                    
                    # make latex string
                    latex_string = make_latex_table_pvalues_reject_fail(df, caption, label, precision)
                    # insert the mean and std keyword
                    mean_to_replace = str(round(mean_to_replace, precision))
                    std_to_replace = str(round(std_to_replace, precision))
                    mean_to_replace_2 = str(round(mean_to_replace_2, precision))
                    std_to_replace_2 = str(round(std_to_replace_2, precision))
                    mean_to_replace = mean_to_replace+" & "+mean_to_replace_2
                    std_to_replace = std_to_replace+" & "+std_to_replace_2
                    if verbose_table:
                        latex_string = latex_string.replace("0"*precision+" & "+ std_to_replace, "0"*precision+" & std " + std_to_replace)
                        latex_string = latex_string.replace("0"*precision+" & "+ mean_to_replace, "0"*precision+" & mean " + mean_to_replace)
                    else:
                        latex_string = latex_string.replace("& "+ std_to_replace,"& std " + std_to_replace)
                        latex_string = latex_string.replace("& "+ mean_to_replace, "& mean " + mean_to_replace)
                    # insert the title
                    latex_string = replace_toprule(latex_string, title)
                    # write latex table
                    save_name = \
                        short_of_slams[slam_idx_1] +"_"+ \
                        short_of_slams[slam_idx_2] +"_"+ \
                        data_type +"_"+ \
                        error_type + \
                        postfix + \
                        verbose_string + ".tex"
                    save_latex_table(
                        latex_string, 
                        folder_save + subfolder_save, 
                        save_name)
                    # end of loop over slams
                # end of loop over slams
            # end of loop over trans rot
        # end of loop over ape rpe

            # check rpe for mean and make new table
            if error_type == "rpe":
                columns = list_slam_repet_trajec_rpe
                for slam_idx_1 in range(0,len(folders)):
                    df = pd.DataFrame()
                    for test_idx in range(0, len(test_names_normal)):
                        list_normal_test_values = normal_test_list(columns[slam_idx_1], test_name = test_names_normal[test_idx])
                        # count the number of pvalues that are above alpha
                        count_fail = sum([1 for i in list_normal_test_values if i > alpha])
                        # count the number of pvalues that are below alpha
                        count_reject = len(list_normal_test_values) - count_fail
                        # make a new column name
                        new_col_name = test_names_normal[test_idx]
                        # put the list of pvalues and the counts in the dataframe
                        if verbose_table:
                            df[new_col_name] = list_normal_test_values + [count_reject, count_fail]
                        else:
                            df[new_col_name] = [count_reject, count_fail]
                        # end of loop over test
                    # name the last two columns reject and fail
                    df.rename(index={len(df)-2: "reject", len(df)-1: "fail"}, inplace=True)
                    postfix = "_norm_check"
                    if verbose_table:
                        verbose_switch_1 = "A column shows the p-values of a hypothesis for 20 tested trajectories. The bottom two rows show"
                        verbose_switch_2 = "effect strength coefficients $f$ and $r$. Their means and standard deviations are in the bottom two rows"
                    else:
                        verbose_switch_1 = "The table shows"
                        verbose_switch_2 = " means and standard deviations of the effect strength coefficients $f$ and $r$"

                    caption = "\caption{Check for normality of %s. %s the counts of rejection and failed rejections. The two columns on the right show the %s. The error measure is the %s \\ac{%s}.}\n" % (
                        names_of_slams[slam_idx_1],
                        verbose_switch_1,
                        verbose_switch_2,
                        data_type_print,
                        error_type)
                    label = "\label{tab:%s_%s_%s_%s}\n" % (
                        names_of_slams[slam_idx_1],
                        data_type, 
                        error_type, 
                        postfix)
                    title = "\multicolumn{%d}{c}{Check for normality %s | error = %s \\ac{%s}}  \\\\ \n \midrule"%(
                        len(test_names_normal), 
                        names_of_slams[slam_idx_1], 
                        data_type_print, 
                        error_type)
                    title = "\multicolumn{%d}{c}{Check for normality %s}\\\\ \multicolumn{%d}{c}{error = %s \\ac{%s}}\\\\ \multicolumn{%d}{c}{significance level $\\alpha$ = %d%s}\\\\"%(
                        len(test_names_normal)+1,  
                        names_of_slams[slam_idx_1],
                        len(test_names_normal)+1,
                        data_type_print, 
                        error_type,
                        len(test_names_normal)+1,
                        alpha*100, "\%")
                    # make latex string
                    latex_string = make_latex_table_pvalues_reject_fail(df, caption, label, precision)
                    latex_string = replace_toprule(latex_string, title)
                    # write latex table
                    save_name = \
                        short_of_slams[slam_idx_1] +"_"+ \
                        data_type +"_"+ \
                        error_type + \
                        postfix + \
                        verbose_string + ".tex"
                    save_latex_table(
                        latex_string, 
                        folder_save + subfolder_save, 
                        save_name)
                    # end of loop over slams
                # end of loop over ape rpe



sys.exit(1)




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
for i in range(0, len(short_of_slams)):
    latex_rpe = latex_rpe.replace('\n'+str(i)+' & ', '\n'+short_of_slams[i]+' & ')
latex_rpe = latex_rpe.replace(' & mean', 'RTE (mm) & mean')
save_latex_table(latex_rpe, folder_save, "rpe", "mean_std_max")
print(latex_rpe)





for error_type in ["ape", "rpe"]:
    if error_type == "ape":
        columns = list_slam_repet_trajec_ape
    else:
        columns = list_slam_repet_trajec_rpe


    for test_idx in range(0, len(test_names)):   
        ### switch test loop and slam loop to get the new table structure ########################################################################################################################################################

        ### make dataframe and calculations ####################################
        df_diff = pd.DataFrame()
        for i in range(0, len(folders)):
            ### switch test loop and slam loop to get the new table structure ################################################################################################################################################
            for j in range(0, i): # begin for loop over slam combinations i!=j
                list_pvalues = hypothesis_test_list(columns[i], columns[j], test_names[test_idx])
                count_fail = sum([1 for i in list_pvalues if i > alpha])
                count_reject = len(list_pvalues) - count_fail
                # new_col_name = names_for_headers[i] + " vs " + names_for_headers[j]
                new_col_name = make_column_header(short_of_slams[i], short_of_slams[j])
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


for error_type in ["ape", "rpe"]:
    if error_type == "ape":
        columns = list_slam_repet_trajec_ape
    else:
        columns = list_slam_repet_trajec_rpe

        
    for test_idx in range(0, len(test_names)):  

        num_of_tests_per_slam = int(num_of_tests_per_slam_combi/2)
        d = num_of_tests_per_slam

        df_self = pd.DataFrame()
        for i in range(0, len(folders)):
            # begin for loop over slams  i==i
            list_pvalues = hypothesis_test_list(columns[i][:d], columns[i][d:], test_names[test_idx])
            count_fail = sum([1 for i in list_pvalues if i > alpha])
            count_reject = len(list_pvalues) - count_fail
            new_col_name = make_column_header(short_of_slams[i], short_of_slams[j])
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