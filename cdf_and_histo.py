import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from util_hypothesis_tests_2 import hypothesis_test_list
from util_hypothesis_tests_2 import read_cols_from_folder
from util_latex_tables import *
from util_error_measures import *
from scipy.stats import norm

# for changing to another simulation scenario the following variables need to be changed:
scenario = "c8"

folders = ["csv/aligned/"+scenario+"_orb_stereo",\
            "csv/aligned/"+scenario+"_orb_d435",\
            "csv/aligned/"+scenario+"_orb_mono"]
# folder_names = folder_names_from_folder_paths(folders)
names_of_slams = ['stereo', 'RGBD', 'mono']
folder_save = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/results/histo_cdf"
if not os.path.exists(folder_save):
    os.makedirs(folder_save)
alpha = 0.05
print_every = False
test_names = ["mwu", "ks2"]
fontsize = 15



def make_cdf(data):
    "np.array with the apes or rpes. return sorted array and cdf values to plot"
    N = len(data)
    x = np.sort(data)
    # get the cdf values of y
    y = np.arange(N) / float(N)
    return x, y

#same but make variable fontsize with 16
fontsize = 16
fontsize_2 = 11
fontsize_legend = 10


#make list of twenty different colors
colors = plt.cm.tab20(np.linspace(0,1,20))
#make 3 line styles
line_styles = ['-', '--', ':']
color_slams = ['black', 'green', 'red']
alpha_histograms = [1.0, 0.5, 1.0]
histtype = ['stepfilled', 'stepfilled', 'step']
linewidth = [1, 1, 1.5]
linewidth_cdf_pairs = 2
cut_y_upper = [0.99, 0.99,1,0.98] # order: xy_ape, xy_rpe, yaw_ape, yaw_rpe
cut_y_lower = [-1, 0.01,0.05,0.02]




sub_y = 5
sub_x = 4
error_idx =- 1
# for data_type rotational or translational a loop
for data_type in ["xy", "yaw"]:
    if data_type == "xy":
        data_type_name = "translational"
        data_unit = "mm"
    else:
        data_type_name = "rotational"
        data_unit = "deg"
    for error_type in ["ape", "rpe"]:
        error_idx+=1
        print(data_type +' '+error_type)
        fig, axs = plt.subplots(2, 1, figsize=(12, 7))
        fig_2, axs_2 = plt.subplots(sub_y, sub_x, figsize=(8, 10))
        fig_3, axs_3 = plt.subplots(sub_y, sub_x, figsize=(8, 10))
        columns = [read_cols_from_folder(folder, data_type +'_'+error_type) for folder in folders] 
        list_slam_concat = []
        for i in range(0, len(columns)):
            list_slam_concat.append(np.concatenate(columns[i]))

        ########################################################## cdfs
        slam_N_x_list = []
        # iterate over all slams
        ymax = 0
        for i in range(0, len(folders)):
            # iterate over all trajectories
            N_x_list =[]
            for j in range(0, len(columns[i])):
                # make cdf
                x, y = make_cdf(columns[i][j])
                #cut x and x such that y is below 0.99
                y = y[y<cut_y_upper[error_idx]]
                x = x[:len(y)]
                y = y[y>cut_y_lower[error_idx]]
                x = x[len(x)-len(y):]
                N_x_list.append(x)
                # plot
                alpha = 0.3
                linewidth = 1.5
                if j == 0 :
                    axs[1].plot(x, y, color=color_slams[i], linestyle=line_styles[i], alpha=alpha, linewidth=linewidth, label=names_of_slams[i] + ' single')
                else:
                    axs[1].plot(x, y, color=color_slams[i], linestyle=line_styles[i], alpha=alpha, linewidth=linewidth)

                #############cdf pairs##############
                axs_2[j//sub_x, j%sub_x].plot(x, y, color=color_slams[i], linestyle=line_styles[i], alpha=1.0, linewidth=linewidth_cdf_pairs, label=names_of_slams[i])
                # title of the plots is the number
                axs_2[j//sub_x, j%sub_x].set_title('CDFs '+str(j))
                # # grid on
                axs_2[j//sub_x, j%sub_x].grid(True)
                # grid in the background
                axs_3[j//sub_x, j%sub_x].set_axisbelow(True)
                # of the most left plots set the y label
                if j%sub_x == 0:
                    axs_2[j//sub_x, j%sub_x].set_ylabel('Cum. Prob.', fontsize=fontsize_2)
                    # make the ticks 0 1
                    axs_2[j//sub_x, j%sub_x].set_yticks([0, 1])
                    #bigger ticks
                    axs_2[j//sub_x, j%sub_x].tick_params(axis='y', which='major', labelsize=fontsize_2)
                # of the most bottom plots set the x label
                if j//sub_x == sub_x:
                    axs_2[j//sub_x, j%sub_x].set_xlabel(error_type.upper() + " ("+data_unit+")", fontsize=fontsize_2)
                    # ticks bigger
                    axs_2[j//sub_x, j%sub_x].tick_params(axis='x', which='major', labelsize=fontsize_2)
                # remove the y ticks of the plots in the middle
                if j%sub_x != 0:
                    # make the ticks invisible
                    axs_2[j//sub_x, j%sub_x].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
                    # and set the y ticks to 0 1
                    axs_2[j//sub_x, j%sub_x].set_yticks([0, 1])
                # remove the x ticks of the plots in the middle
                if j//sub_x != sub_x:
                    # make the ticks invisible
                    axs_2[j//sub_x, j%sub_x].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
                # make a legende in the upper left plot
                if j == 0:
                    axs_2[j//sub_x, j%sub_x].legend(loc='upper left', fontsize=fontsize_legend)
                
                ############# histo pairs ##############
                # make a histogram
                k_rice = int(2 * len(x)**(1/3))
                n,_,_ = axs_3[j//sub_x, j%sub_x].hist(x, bins=k_rice, density=True, 
                    histtype=histtype[i], color=color_slams[i], alpha=alpha_histograms[i], label=names_of_slams[i], linewidth=linewidth, 
                    edgecolor= color_slams[i])
                
                if ymax < np.max(n):
                    ymax = np.max(n)
                # set the y limit
                axs_3[j//sub_x, j%sub_x].set_ylim(0.0, ymax)
                # title of the plots is the number
                axs_3[j//sub_x, j%sub_x].set_title('Histogram '+str(j))
                # # grid on
                axs_3[j//sub_x, j%sub_x].grid(True)
                # grid in the background
                axs_3[j//sub_x, j%sub_x].set_axisbelow(True)
                # of the most left plots set the y label
                if j%sub_x == 0:
                    axs_3[j//sub_x, j%sub_x].set_ylabel('Prob.', fontsize=fontsize_2)
                    #bigger ticks
                    axs_3[j//sub_x, j%sub_x].tick_params(axis='y', which='major', labelsize=fontsize_2)
                # of the most bottom plots set the x label
                if j//sub_x == sub_x:
                    axs_3[j//sub_x, j%sub_x].set_xlabel(error_type.upper() + " ("+data_unit+")", fontsize=fontsize_2)
                    # ticks bigger
                    axs_3[j//sub_x, j%sub_x].tick_params(axis='x', which='major', labelsize=fontsize_2)
                # remove the y ticks of the plots in the middle
                if j%sub_x != 0:
                    # make the ticks invisible
                    axs_3[j//sub_x, j%sub_x].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
                # remove the x ticks of the plots in the middle
                if j//sub_x != sub_x:
                    # make the ticks invisible
                    axs_3[j//sub_x, j%sub_x].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
                # make a legende in the upper left plot
                if j == 0:
                    axs_3[j//sub_x, j%sub_x].legend(loc='upper left', fontsize=fontsize_legend)

        slam_N_x_list.append(N_x_list)
        #iterate over all slams again
        for i in range(0, len(folders)):
            #again iterate over trajectories again
            for j in range(0, len(columns[i])):
                axs_3[j//sub_x, j%sub_x].set_ylim(0.0, ymax)


        axs[1].set_xlabel(error_type.upper() + " ("+data_unit+")", fontsize=fontsize)
        axs[1].set_ylabel('Cumulative Probability', fontsize=fontsize)
        # plt.legend()
        axs[1].set_title('Scenario '+scenario+', '+data_type_name+' '+error_type.upper()+': Empirical CDFs of every trajectory and of all trajectories merged', fontsize=fontsize)

        slam_concat_x_list = []
        linewidth = 5
        for i in range(0, len(list_slam_concat)):
            # make cdf
            x, y = make_cdf(list_slam_concat[i])
            #cut x and x such that y is below 0.99
            y = y[y<cut_y_upper[error_idx]]
            x = x[:len(y)]
            y = y[y>cut_y_lower[error_idx]]
            x = x[len(x)-len(y):]
            slam_concat_x_list.append(x)
            # plot
            axs[1].plot(x, y, color=color_slams[i], linestyle=line_styles[i], linewidth=linewidth, alpha = 1.0, label=names_of_slams[i] + ' merged')

        #legende in lower right corner
        axs[1].legend(loc='lower right', fontsize=fontsize)
        axs[1].tick_params(axis='both', which='major', labelsize=fontsize)
        axs[1].tick_params(axis='both', which='minor', labelsize=fontsize)

        ########################################################### histogram

        post_fix_label = ' merged'
        # k of rice
        # get the length of every ape array in list_slam_concat
        N = [len(slam_concat_x_list[i]) for i in range(0, len(slam_concat_x_list))]
        # make individual k_rice for every list_slam_concat
        k_rice = [int(2 * N[i]**(1/3)) for i in range(0, len(slam_concat_x_list))]
        #make histogram with k_rice bins for concatenated ape arrays
        n_0,_,_ = axs[0].hist(slam_concat_x_list[0], bins=k_rice[0], density=True, 
                    histtype='stepfilled', color='black', 
                    label=names_of_slams[0]+post_fix_label, linewidth=1.5)
        
        n_1,_,_ = axs[0].hist(slam_concat_x_list[1], bins=k_rice[1], density=True, 
                    histtype='stepfilled', color='green', alpha=0.5, label=names_of_slams[1]+post_fix_label, linewidth=2, 
                    edgecolor= 'darkgreen')

        n_2,_,_ = axs[0].hist(slam_concat_x_list[1], bins=k_rice[1], density=True, 
                    histtype='step', color='green', alpha=1.0, linewidth=2, 
                    edgecolor= 'darkgreen')

        n_3,_,_ = axs[0].hist(slam_concat_x_list[2], bins=k_rice[2], density=True, 
                    histtype='step', color='red', alpha=1.0, 
                    label=names_of_slams[2]+post_fix_label, linewidth=1.5, zorder=10)
        n = [n_0, n_1, n_2, n_3]
        n = [np.max(n[i]) for i in range(0, len(n))]
        n_max = np.max(n)
        axs[0].set_ylim(0.0, n_max*1.05)
        axs[0].set_title("Scenario "+scenario+" "+data_type_name+" "+error_type.upper()+": Histogram of the errors merged over all trajectories",fontsize=fontsize)
        axs[0].set_xlabel(error_type.upper()+" ("+data_unit+")", fontsize=fontsize)
        axs[0].set_ylabel("Probability", fontsize=fontsize)
        axs[0].tick_params(axis='both', which='major', labelsize=fontsize)
        axs[0].tick_params(axis='both', which='minor', labelsize=fontsize)
        #get the max value of the histogram  
        #get axis limits of plot above
        xmin, xmax = axs[1].get_xlim()
        #set axis limits of plot below
        axs[0].set_xlim(xmin, xmax)
        # if rpe get mean and std of the x_list elements
        # if error_type == "rpe":
        #     for i in range(0, len(x_list)):
        #         mu = np.mean(x_list[i])
        #         sigma =np.std(x_list[i])
        #         #plot a normal distribution with mu and sigma
        #         x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
        #         axs[0].plot(x, norm.pdf(x, mu, sigma), color=color_slams[i], linestyle=line_styles[i], linewidth=linewidth/2, alpha = 0.6, label=names_of_slams[i] + ' normal pdf')
        axs[0].legend(fontsize=fontsize)


        # save plot as pdf in folder save
        plt.figure(fig.number)
        plt.tight_layout()
        plt.savefig(os.path.join(folder_save, scenario +'_'+data_type +'_'+error_type + '_cdfs_histo.pdf'), bbox_inches='tight')
        # save fig_2
        plt.figure(fig_2.number)
        #set the title of the figure
        fig_2.suptitle("Scenario "+scenario+" "+data_type_name+" "+error_type.upper()+": Empirical CDFs of every trajectory pair", fontsize=fontsize)
        plt.tight_layout()
        plt.savefig(os.path.join(folder_save, scenario +'_'+data_type +'_'+error_type + '_all_cdf_pairs.pdf'), bbox_inches='tight')
        # save fig_3
        plt.figure(fig_3.number)
        #set the title of the figure
        fig_3.suptitle("Scenario "+scenario+" "+data_type_name+" "+error_type.upper()+": Histogram of the errors of every trajectory pair", fontsize=fontsize)
        plt.tight_layout()
        plt.savefig(os.path.join(folder_save, scenario +'_'+data_type +'_'+error_type + '_all_histo_pairs.pdf'), bbox_inches='tight')

        # plt.show()





