import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import os


folder_1 = "/home/dino/figures"
folder_2 = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/figures"
save_name = 'c4_orb_s1_d1'
save_name_fig_1 = save_name + '_hist_eucl.pdf'
save_name_fig_2 = save_name + '_hist_xy.pdf'
save_name_fig_3 = save_name + '_over_time.pdf'

fontsize_xlabel = 14
fontsize_ylabel = fontsize_xlabel
labelsize_axes = 13
fontsize_title = 16
fontsize_legend = 12
linewidth_gt = 2
linewidth_data = 2
suptitle = 'ORB SLAM3 stereo vs rgbd' # overall title on the very top
color_list = ['red', 'black', 'blue', 'green', 'orange', 'purple', 'pink', 'cyan', 'yellow']

bins_x_number = 50
bins_y_number = bins_x_number
bins_x = np.linspace(-0.15,0.15,bins_x_number)
bins_y = np.linspace(-0.1,0.1,bins_y_number)

bins_euclidean_number = 50
bins_euclidean_delta_number = bins_euclidean_number 
bins_euclidean = np.linspace(0,0.15,bins_euclidean_number)
bins_euclidean_delta = np.linspace(-0.1,0.1,bins_euclidean_delta_number)



plt.rc('axes', axisbelow=True)

df_list = []
df_type_list = []
df_type_name_list = ['ground_truth', 'mono', 'stereo', 'd435', 'unknown']
# import arbitrary number of csv files from csv/aligned
for i in range(1, len(sys.argv)):
    df_list.append(pd.read_csv(sys.argv[i]))
    # split at _vs_ and take the last part
    last_part_of_arg = sys.argv[i].split('_vs_')[-1]
    last_part_of_arg = last_part_of_arg.replace('.csv', '')
    last_part_of_arg = last_part_of_arg.replace('-bag', '')
    df_type_list.append(last_part_of_arg)


# calculate the euclidean distance between the ground truth and the data without z
for i in range(len(df_list)):
    df_list[i]['euclidean_distance'] = ((df_list[i]['x'] - df_list[i]['x_gt'])**2 + (df_list[i]['y'] - df_list[i]['y_gt'])**2)**0.5
    # diff too
    df_list[i]['euclidean_distance_delta'] = df_list[i]['euclidean_distance'].diff()
# put all the euclidean_distance and euclidean_distance_delta into a list as np.array
euclidean_distance_list = []
euclidean_distance_delta_list = []
for i in range(len(df_list)):
    euclidean_distance_list.append(df_list[i]['euclidean_distance'].to_numpy())
    euclidean_distance_delta_list.append(df_list[i]['euclidean_distance_delta'].to_numpy())
#plot histogram of euclidean distance and euclidean distance delta in subplot
fig_1, ax = plt.subplots(2, 1)
fig_1.suptitle(suptitle)
ax[0].yaxis.grid(color='gray', linestyle='dashed')
# ax[0].hist(df['euclidean_distance'], bins=100)
ax[0].set_title('Euclidean distance')
ax[0].set_xlabel('euclidean distance', fontsize=fontsize_xlabel)
ax[0].set_ylabel('frequency', fontsize=fontsize_ylabel)
ax[1].yaxis.grid(color='gray', linestyle='dashed')
# ax[1].hist(df['euclidean_distance_delta'], bins=100)
ax[1].set_title('First discrete difference of euclidean distance')
ax[1].set_xlabel('distance delta', fontsize=fontsize_xlabel)
ax[1].set_ylabel('frequency', fontsize=fontsize_ylabel)
ax[0].tick_params(axis='both', which='major', labelsize=labelsize_axes)
ax[1].tick_params(axis='both', which='major', labelsize=labelsize_axes)
# set the axis limits to -0.15,0.15
# ax[0].set_xlim(0,0.15)
# ax[1].set_xlim(-0.1,0.1)
# plot the histogram of euclidean distance and euclidean distance delta in subplot
ax[0].hist(euclidean_distance_list, bins=bins_euclidean, color=color_list[0:len(euclidean_distance_list)])
ax[1].hist(euclidean_distance_delta_list, bins=bins_euclidean_delta, color=color_list[0:len(euclidean_distance_delta_list)])
ax[0].legend(df_type_list)
ax[1].legend(df_type_list)
fig_1.tight_layout(h_pad=2)
# plt.show()

# #calculate the difference between the x and y columns of the ground truth and the data
for i in range(len(df_list)):
    df_list[i]['x_diff'] = df_list[i]['x'] - df_list[i]['x_gt']
    df_list[i]['y_diff'] = df_list[i]['y'] - df_list[i]['y_gt']
# put all the x_diff and y_diff into a list as np.array
x_diff_list = []
y_diff_list = []
for i in range(len(df_list)):
    x_diff_list.append(df_list[i]['x_diff'].to_numpy())
    y_diff_list.append(df_list[i]['y_diff'].to_numpy())
#plot histogram of x_diff and y_diff in subplot
fig_2, ax = plt.subplots(2, 1)
fig_2.suptitle(suptitle)
ax[0].yaxis.grid(color='gray', linestyle='dashed')
# ax[0].hist(df['x_diff'], bins=100)
ax[0].set_title('Signed distance to ground truth in x dimension')
ax[0].set_xlabel('distance in x', fontsize=fontsize_xlabel)
ax[0].set_ylabel('frequency', fontsize=fontsize_ylabel)
ax[1].yaxis.grid(color='gray', linestyle='dashed')
# ax[1].hist(df['y_diff'], bins=100)
ax[1].set_title('Signed distance to ground truth in y dimension')
ax[1].set_xlabel('distance in y', fontsize=fontsize_xlabel)
ax[1].set_ylabel('frequency', fontsize=fontsize_ylabel)
ax[0].tick_params(axis='both', which='major', labelsize=labelsize_axes)
ax[1].tick_params(axis='both', which='major', labelsize=labelsize_axes)
# ax[0].set_xlim(-0.15,0.15)
# ax[1].set_xlim(-0.1,0.1)
# plot the histogram of x_diff and y_diff in subplot
ax[0].hist(x_diff_list, bins=bins_x, color=color_list[0:len(x_diff_list)])
ax[1].hist(y_diff_list, bins=bins_y, color=color_list[0:len(y_diff_list)])
ax[0].legend(df_type_list)
ax[1].legend(df_type_list)
fig_2.tight_layout(h_pad=2)
# plt.show()

# plot the diffs against the time stamp
fig_3, ax = plt.subplots(3, 1)
fig_3.suptitle(suptitle)
ax[0].yaxis.grid(color='gray', linestyle='dashed')
# ax[0].plot(df['stamp'], df['x_diff'])
ax[0].set_title('Signed distance to ground truth in x dimension')
ax[0].set_xlabel('time', fontsize=fontsize_xlabel)
ax[0].set_ylabel('distance in x', fontsize=fontsize_ylabel)
ax[1].yaxis.grid(color='gray', linestyle='dashed')
# ax[1].plot(df['stamp'], df['y_diff'])
ax[1].set_title('Signed distance to ground truth in y dimension')
ax[1].set_xlabel('time', fontsize=fontsize_xlabel)
ax[1].set_ylabel('distance in y', fontsize=fontsize_ylabel)
ax[0].tick_params(axis='both', which='major', labelsize=labelsize_axes)
ax[1].tick_params(axis='both', which='major', labelsize=labelsize_axes)
ax[2].yaxis.grid(color='gray', linestyle='dashed')
# ax[2].plot(df['stamp'], df['euclidean_distance'])
ax[2].set_title('Euclidean distance to ground truth')
ax[2].set_xlabel('time', fontsize=fontsize_xlabel)
ax[2].set_ylabel('euclidean distance', fontsize=fontsize_ylabel)
ax[2].tick_params(axis='both', which='major', labelsize=labelsize_axes)
# do it for all the other dataframes
for i in range(len(df_list)):
    ax[0].plot(df_list[i]['stamp'], df_list[i]['x_diff'], color=color_list[i])
    ax[1].plot(df_list[i]['stamp'], df_list[i]['y_diff'], color=color_list[i])
    ax[2].plot(df_list[i]['stamp'], df_list[i]['euclidean_distance'], color=color_list[i])
# make the figure larger in height
fig_3.set_figheight(8)
ax[0].legend(df_type_list)
ax[1].legend(df_type_list)
ax[2].legend(df_type_list)
fig_3.tight_layout(h_pad=1)




plt.show(block=False)

# save the figures
print('--------------------------------------')
# figure 1
if os.path.exists(folder_2 + '/' + save_name_fig_1):
    prompt = input("If you want to overwrite " + save_name_fig_1 + " type 'y' and enter: ")
    if prompt == 'y':
        fig_1.savefig(folder_2 + '/' + save_name_fig_1)
        # fig_1.savefig(folder_1 + '/' + save_name_fig_1)
        print("saved: " + save_name_fig_1)
    else:
        print("did not save: " + save_name_fig_1)
else:
    prompt = input("If you want to save " + save_name_fig_1 + " type 'y' and enter: ")
    if prompt == 'y':
        fig_1.savefig(folder_2 + '/' + save_name_fig_1)
        # fig_1.savefig(folder_1 + '/' + save_name_fig_1)
        print("saved: " + save_name_fig_1)
    else:
        print("did not save: " + save_name_fig_1)
# figure 2
if os.path.exists(folder_2 + '/' + save_name_fig_2):
    prompt = input("If you want to overwrite " + save_name_fig_2 + " type 'y' and enter: ")
    if prompt == 'y':
        fig_2.savefig(folder_2 + '/' + save_name_fig_2)
        # fig_2.savefig(folder_1 + '/' + save_name_fig_2)
        print("saved: " + save_name_fig_2)
    else:
        print("did not save: " + save_name_fig_2)
else:
    prompt = input("If you want to save " + save_name_fig_2 + " type 'y' and enter: ")
    if prompt == 'y':
        fig_2.savefig(folder_2 + '/' + save_name_fig_2)
        # fig_2.savefig(folder_1 + '/' + save_name_fig_2)
        print("saved: " + save_name_fig_2)
    else:
        print("did not save: " + save_name_fig_2)
# figure 3
if os.path.exists(folder_2 + '/' + save_name_fig_3):
    prompt = input("If you want to overwrite " + save_name_fig_3 + " type 'y' and enter: ")
    if prompt == 'y':
        fig_3.savefig(folder_2 + '/' + save_name_fig_3)
        # fig_3.savefig(folder_1 + '/' + save_name_fig_3)
        print("saved: " + save_name_fig_3)
    else:
        print("did not save: " + save_name_fig_3)
else:
    prompt = input("If you want to save " + save_name_fig_3 + " type 'y' and enter: ")
    if prompt == 'y':
        fig_3.savefig(folder_2 + '/' + save_name_fig_3)
        # fig_3.savefig(folder_1 + '/' + save_name_fig_3)
        print("saved: " + save_name_fig_3)
    else:
        print("did not save: " + save_name_fig_3)

print("Segmentation fault in next line from plt.show() is normal.")


