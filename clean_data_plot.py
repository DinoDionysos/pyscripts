import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import sys
import os

folder_1 = "/home/dino/figures"
folder_2 = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/figures"

save_name = 'c4_orb_s1_gt.pdf'
save_name_path = '/home/dino/figures/' + save_name; 
title = 'Trajectory: ORB SLAM3 stereo vs. Ground Truth'

# for small figure, f.ex. for subfigures half page
fontsize_xlabel = 14
fontsize_ylabel = fontsize_xlabel
labelsize_axes = 13
fontsize_title = 16
fontsize_legend = 12
linewidth_gt = 2
linewidth_data = 2
linestyle_gt = 'solid'
# linestyle_data = (0,(3,1))
linestyle_data = 'solid'
color_list = ['red', 'black', 'blue', 'green', 'orange', 'purple', 'pink', 'cyan', 'yellow']


file_name = os.path.basename(__file__)
csv_path_list = []
csv_type_list = []
csv_type_name_list = ['ground_truth', 'mono', 'stereo', 'd435', 'unnamed']

# read a dynamic number of input arguments
for i in range(1, len(sys.argv)):
    csv_path_list.append(sys.argv[i])
    # split them at 'odom' and take the last part
    last_part_of_arg = sys.argv[i].split('odom')[-1]
    # check if the last part of the argument has one of the csv_type_names in it
    j = 0
    type = 4
    for csv_type_name in csv_type_name_list:
        if csv_type_name in last_part_of_arg:
            type = j
            break
        j += 1
    if type == 4:
        print("[INFO] "+file_name+" | The last part of argument: " + sys.argv[i] + " (" + sys.argv[i].split('odom')[-1] + ") does not contain ground_truth, mono, stereo or d435 in it. Please rename the file accordingly.")
    csv_type_list.append(type)

df_list = []
for i in range(len(csv_path_list)):
    df_list.append(pd.read_csv(csv_path_list[i]))

# do the same again but without subplot and withpout timestamps
fig, ax = plt.subplots(1, 1)
fig.tight_layout(h_pad=2)
ax.set_title(title, fontsize=fontsize_title)
ax.set_xlabel('x in meters', fontsize=fontsize_xlabel)
ax.set_ylabel('y in meters', fontsize=fontsize_ylabel)
# make label size bigger
ax.tick_params(axis='both', which='major', labelsize=labelsize_axes)


# fig.suptitle('ORB SLAM3 d435 vs Ground Truth')
plt.subplots_adjust(top=0.92)
plt.axis('equal')
# add a grid
# plt.grid()
# plt.subplots_adjust(hspace=0.6)

df_x_list = []
df_y_list = []
legend_list_2 = []
for i in range(len(df_list)):
    df_x_list.append(df_list[i]['x'].to_numpy())
    df_y_list.append(df_list[i]['y'].to_numpy())
    # normalize the x and y columns
    df_x_list[i] = df_x_list[i] - df_x_list[i][0]
    df_y_list[i] = df_y_list[i] - df_y_list[i][0]
    # do the scaling only for mono
    if csv_type_list[i] == 1:
        # get max value of x and y
        max_x = max(df_x_list[i])
        max_y = max(df_y_list[i])
        # scale dataset times the ratio
        df_x_list[i] = df_x_list[i] / max_x
        df_y_list[i] = df_y_list[i] / max_y
    legend_list_2.append(csv_type_name_list[csv_type_list[i]])
# add the gt from the first csv file at the beginning and no scaling for mono
df_x_list.insert(0, df_list[0]['x_gt'].to_numpy())
df_y_list.insert(0, df_list[0]['y_gt'].to_numpy())
#normalize the x and y columns
df_x_list[0] = df_x_list[0] - df_x_list[0][0]
df_y_list[0] = df_y_list[0] - df_y_list[0][0]
legend_list_2.insert(0, csv_type_name_list[0])

idx_until = -1
idx_from = 0
for i in range(len(df_x_list)):
    if i == 0:
        ax.plot(df_x_list[i][idx_from:idx_until], df_y_list[i][idx_from:idx_until], color=color_list[i], label=legend_list_2[i], linewidth=linewidth_gt, linestyle=linestyle_gt)
    else:
        ax.plot(df_x_list[i][idx_from:idx_until], df_y_list[i][idx_from:idx_until], color=color_list[i], label=legend_list_2[i], linewidth=linewidth_data, linestyle=linestyle_data)
# plot a green x at 0,0
# ax.plot(0, 0, color='green', marker='x', linestyle='none', markersize=10)
ax.legend(legend_list_2, fontsize=fontsize_legend)
fig.tight_layout(h_pad=2)

# show the plot and make it possible to save it during it is shown
plt.show(block=False)
# save the plot if prompt is 'y'. if prompt is 'n' do not save the plot. show the save_name in the question
#check if the save_name_path already exists
print('------------------------------------------------------------------------------------')
if os.path.exists(save_name_path):
    prompt = input("The file " + save_name + " already exists. If you want to overwrite it, type 'y' and enter: ")
    if prompt == 'y':
        fig.savefig(save_name_path)
        fig.savefig(folder_2 + "/" + save_name)
        print("saved: " + save_name)
    else:
        print("did not save: " + save_name)
else:
    prompt = input("If you want to save the plot to " + save_name + ", type 'y' and enter: ")
    if prompt == 'y':
        fig.savefig(save_name_path)
        fig.savefig(folder_2 + "/" + save_name)
        print("saved: " + save_name)
    else:
        print("did not save: " + save_name)
print("Segmentation fault in next line from plt.show() is normal.")


