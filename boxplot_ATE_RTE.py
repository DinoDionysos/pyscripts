import os
import numpy as np
from matplotlib import pyplot as plt
import sys

from util_hypothesis_tests_2 import read_cols_from_folder
from util_error_measures import *
from util_latex_tables import *
from util import type_yes_to_save

#make dictionary with names of the scenarios
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

# scenarios_num = [9, 15, 28, 19, 17, 51, 49, 34]
scenarios_num = [9, 15, 28, 19, 17, 51, 49, 34]
scenarios = ["c"+str(i) for i in scenarios_num]
if save_flag:
    print("########## BOXPLOTS PERCENTILES BOXPLOTS PERCENTILES BOXPLOTS PERCENTILES #############")
    save_flag = type_yes_to_save(save_flag, scenarios)
else:
    print("No plots and tables will be saved.")   
    sys.exit(1)  

fontsize = 20
c=-1
for scenario in scenarios:
    c+=1
    folder_latex_inputs_fig_caption_labels = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/inputs/input_results/fig_captions_labels/" + scenario + "/"
    if not os.path.exists(folder_latex_inputs_fig_caption_labels):
        os.makedirs(folder_latex_inputs_fig_caption_labels)
    
    print('scenario', scenario)
    folder_results_win = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/results/"
    folder_results_ssd = "/mnt/d/results/"
    folder_save = folder_results_win + scenario + "/ate_rte/"
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


    for trans_rot_idx in range(0,2):
        if trans_rot_idx == 0:
            list_slam_repet_trajec_ape = [read_cols_from_folder(folder, "xy_ape") for folder in folders] 
            list_slam_repet_trajec_rpe = [read_cols_from_folder(folder, "xy_rpe") for folder in folders]
            data_type = "xy"
            data_type_print = "translational"
            data_type_print_short = "trans."
            unit = "mm"
            precision_rte = 2
            precision_ate = 2
        else:
            list_slam_repet_trajec_ape = [read_cols_from_folder(folder, "yaw_ape") for folder in folders] 
            list_slam_repet_trajec_rpe = [read_cols_from_folder(folder, "yaw_rpe") for folder in folders]
            data_type = "yaw"
            data_type_print = "rotational"
            data_type_print_short = "rot."
            unit = "deg"
            precision_rte = 3
            precision_ate = 3

        # for with index over ape rpe
        for ate_rte_idx in range(0,2):
            if ate_rte_idx == 0:
                list_slam_repet_trajec = list_slam_repet_trajec_ape
                ate_rte = "ate"
                list_slam_repet_ate_rte = [ates_from_columns(list_slam_repet_trajec[i]) for i in range(0, len(list_slam_repet_trajec))]
            else:
                list_slam_repet_trajec = list_slam_repet_trajec_rpe
                ate_rte = "rte"
                # list length #slams with arrays length N with T ate elements
                # N ates pro SLAM
                list_slam_repet_ate_rte = [ates_from_columns(list_slam_repet_trajec[i]) for i in range(0, len(list_slam_repet_trajec))]




            # from here make boxplots instead of tables with mean, std and max
            # figure for boxplot with the ate of all slams side by side
            fig = plt.figure()
            plt.ylabel(data_type_print+' '+ate_rte.upper()+' ('+unit+')', fontsize=fontsize)
            for i in range(0, len(list_slam_repet_ate_rte)): # loop over slams
                #plot boxplot of ate for slam i in figure
                # plt.boxplot(list_slam_repet_ate_rte[i], positions=[i])
                #increase linewidth
                plt.boxplot(list_slam_repet_ate_rte[i],
                             whis=(5,95), 
                             positions=[i], 
                             widths=0.5, 
                             boxprops=dict(linewidth=2), 
                             medianprops=dict(linewidth=2), 
                             whiskerprops=dict(linewidth=2), 
                             capprops=dict(linewidth=2))
            plt.xticks(np.arange(0, len(list_slam_repet_ate_rte)), short_of_slams)
            plt.tick_params(axis='both', which='major', labelsize=fontsize)
            plt.tight_layout()
            if save_flag:
                fig.savefig(folder_save+scenario+"_boxplot_"+data_type+"_"+ate_rte+".pdf")
            caption = "Boxplots of the "+data_type_print+" \\ac{"+ate_rte+"} for all three ORB-SLAM types. The whiskers are the 5 and 95 percentile. The box is the 25 and 75 percentile. The red line is the median."
            label = "fig:"+scenario+"_"+data_type+"_"+ate_rte+"_histo"
            caption_label = add_caption_label_to_latex_string("", caption, label)
            if save_flag:
                save_latex_table(
                    caption_label, 
                    folder_latex_inputs_fig_caption_labels, 
                    scenario+"_boxplot_"+data_type+"_"+ate_rte+".tex")
            # plt.show(block=False)

            percentiles = [5, 25, 50, 75, 95]
            # make mean and std of ate. list of length #slams
            # ATE mean über alle N Trajektorien for alle slam
            list_slam_ate_mean_min = [np.min(list_slam_repet_ate_rte[i]) for i in range(0, len(list_slam_repet_ate_rte))]
            list_slam_ate_mean_p5 = [np.percentile(list_slam_repet_ate_rte[i],5) for i in range(0, len(list_slam_repet_ate_rte))]
            list_slam_ate_mean_p25 = [np.percentile(list_slam_repet_ate_rte[i],25) for i in range(0, len(list_slam_repet_ate_rte))]
            list_slam_ate_mean_p50 = [np.percentile(list_slam_repet_ate_rte[i],50) for i in range(0, len(list_slam_repet_ate_rte))]
            list_slam_ate_mean_p75 = [np.percentile(list_slam_repet_ate_rte[i],75) for i in range(0, len(list_slam_repet_ate_rte))]
            list_slam_ate_mean_p95 = [np.percentile(list_slam_repet_ate_rte[i],95) for i in range(0, len(list_slam_repet_ate_rte))]
            list_slam_ate_mean_max = [np.max(list_slam_repet_ate_rte[i]) for i in range(0, len(list_slam_repet_ate_rte))]

            # make dataframe from list_slam_ate_mean
            df_ate = pd.DataFrame()
            df_ate["max"] = list_slam_ate_mean_max
            df_ate["95\%"] = list_slam_ate_mean_p95
            df_ate["75\%"] = list_slam_ate_mean_p75
            df_ate["50\%"] = list_slam_ate_mean_p50
            df_ate["25\%"] = list_slam_ate_mean_p25
            df_ate["5\%"] = list_slam_ate_mean_p5
            df_ate["min"] = list_slam_ate_mean_min
            # flip the df_ate such that the cols are the rows
            df_ate = df_ate.transpose()
            #change the column names
            df_ate.columns = short_of_slams
            # name the index column "percentile"
            # df_ate.index.name = "p"
            # to latex
            latex_ate = df_ate.to_latex(float_format=f'%.{precision_ate}f')
            for i in range(0, len(short_of_slams)):
                latex_ate = latex_ate.replace('\n'+str(i)+' & ', '\n'+short_of_slams[i]+' & ')
            # replace "\toprule \\ & mean" with "\toprule \\ ATE (mm) & mean"
            # latex_ate = latex_ate.replace(' & mean', data_type_print_short+' ATE ('+unit+') & mean')
            caption = "5, 25, 50, 75 and 95 percentiles of the \\ac{"+ate_rte+"} for "+data_type_print+" error data. The percentiles are the respective values of the boxplot in (a). The minimum and maximum values are the dots in the boxplot."
            label = "tab:"+scenario+"_"+data_type+"_"+ate_rte+"_percentiles"
            latex_ate_caption_label = add_caption_label_to_latex_string("", caption, label)
            # Translational Mean, Standard Deviation and the maximal value of the
            if save_flag:
                save_latex_table(latex_ate, folder_save, scenario +"_"+ data_type+"_"+ ate_rte +"_percentiles.tex")
            
            
            if save_flag:
                save_latex_table(
                    latex_ate_caption_label, 
                    folder_latex_inputs_fig_caption_labels, 
                    scenario+"_"+data_type+"_"+ate_rte+"_percentiles.tex")

            caption_main = "Scenario "+ scenario_names[scenarios_num[c]] +": Boxplots (a) and the respective values of the precentiles (b) of the "+data_type_print+" \\ac{"+ate_rte+"} for all three ORB-SLAM types."
            label_main = "fig:"+scenario+"_"+data_type+"_"+ate_rte
            caption_label = add_caption_label_to_latex_string("", caption_main, label_main)
            if save_flag:
                save_latex_table(
                    caption_label, 
                    folder_latex_inputs_fig_caption_labels, 
                    scenario+"_"+data_type+"_"+ate_rte+".tex")
            
            


# plt.show()


