import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import sys
import os

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
ax.set_title('Trajectory: ORB SLAM3 d435 vs Ground Truth')
ax.set_xlabel('x in meters')
ax.set_ylabel('y in meters')

# fig.suptitle('ORB SLAM3 d435 vs Ground Truth')
plt.subplots_adjust(top=0.92)
plt.axis('equal')
# add a grid
# plt.grid()
# plt.subplots_adjust(hspace=0.6)

df_x_list = []
df_y_list = []
legend_list_2 = []
# for i in range(len(df_list)):
#     df_x_list.append(df_list[i]['x'].to_numpy())
#     df_y_list.append(df_list[i]['y'].to_numpy())
#     df_x_list.append(df_list[i]['x_gt'].to_numpy())
#     df_y_list.append(df_list[i]['y_gt'].to_numpy())
#     # normalize the x and y columns
#     df_x_list[2*i] = df_x_list[2*i] - df_x_list[2*i][0]
#     df_y_list[2*i] = df_y_list[2*i] - df_y_list[2*i][0]
#     df_x_list[2*i+1] = df_x_list[2*i+1] - df_x_list[2*i+1][0]
#     df_y_list[2*i+1] = df_y_list[2*i+1] - df_y_list[2*i+1][0]
#     # do the scaling only for mono
#     if csv_type_list[i] == 1:
#         # get max value of x and y
#         max_x = max(df_x_list[2*i])
#         max_y = max(df_y_list[2*i])
#         # scale dataset times the ratio
#         df_x_list[2*i] = df_x_list[2*i] / max_x
#         df_y_list[2*i] = df_y_list[2*i] / max_y
#     legend_list_2.append(csv_type_name_list[csv_type_list[i]])
#     legend_list_2.append(csv_type_name_list[0])
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
color_list = ['black', 'red', 'green', 'orange', 'purple', 'pink', 'cyan', 'yellow']
# for i in range(len(df_x_list)):
#     ax.plot(df_x_list[i][idx_from:idx_until], df_y_list[i][idx_from:idx_until], color=color_list[i], marker='o', markeredgecolor='black')
# do the same but for the first bigger size
for i in range(len(df_x_list)):
    if i == 0:
        ax.plot(df_x_list[i][idx_from:idx_until], df_y_list[i][idx_from:idx_until], color=color_list[i], label=legend_list_2[i], linewidth=1)
    else:
        ax.plot(df_x_list[i][idx_from:idx_until], df_y_list[i][idx_from:idx_until], color=color_list[i], label=legend_list_2[i])
# plot a green x at 0,0
# ax.plot(0, 0, color='green', marker='x', linestyle='none', markersize=10)
# ax.legend(legend_list_2)
fig.tight_layout(h_pad=2)
plt.show()



# for i in range(len(df_x_list)):
    # ax.plot(df_x_list[i][idx_from:idx_until], df_y_list[i][idx_from:idx_until], color=color_list[i], marker='o', markeredgecolor='black')

# first plot for timestamps
# fig, ax = plt.subplots(1, 1, gridspec_kw={'height_ratios': [1, 7]})
# fig.tight_layout(h_pad=2)
# ax[0].set_title('Timestamps')
# ax[0].set_xlabel('time')
# ax[0].axes.get_yaxis().set_visible(False)
# legend_list = []
# color_list = ['blue', 'red', 'green', 'orange', 'purple', 'pink', 'cyan', 'yellow']

# # for all the csv files in the list
# for i in range(len(df_list)):
#     # get the timestamp column
#     df_timestamp = df_list[i]['stamp']
#     # normalize the timestamp column
#     df_timestamp = df_timestamp - df_timestamp[0]
#     #convert to numpy array
#     df_timestamp = df_timestamp.to_numpy()
#     # make arry of ones
#     ones = np.ones(len(df_timestamp))
#     # plot the timestamp
#     ax[0].plot(df_timestamp, ones, color=color_list[i], marker='o', linestyle='none')
#     legend_list.append(csv_type_name_list[csv_type_list[i]])

# ax[0].legend(legend_list)

# # second plot
# ax[1].set_title('Trajectory')
# ax[1].set_xlabel('x')
# ax[1].set_ylabel('y')

# fig.suptitle('ORB SLAM3 vs Ground Truth')
# plt.subplots_adjust(top=0.92)
# plt.axis('equal')
# # plt.subplots_adjust(hspace=0.6)

# df_x_list = []
# df_y_list = []
# legend_list_2 = []
# for i in range(len(df_list)):
#     df_x_list.append(df_list[i]['x'].to_numpy())
#     df_y_list.append(df_list[i]['y'].to_numpy())
#     df_x_list.append(df_list[i]['x_gt'].to_numpy())
#     df_y_list.append(df_list[i]['y_gt'].to_numpy())
#     # normalize the x and y columns
#     df_x_list[2*i] = df_x_list[2*i] - df_x_list[2*i][0]
#     df_y_list[2*i] = df_y_list[2*i] - df_y_list[2*i][0]
#     df_x_list[2*i+1] = df_x_list[2*i+1] - df_x_list[2*i+1][0]
#     df_y_list[2*i+1] = df_y_list[2*i+1] - df_y_list[2*i+1][0]
#     # do the scaling only for mono
#     if csv_type_list[i] == 1:
#         # get max value of x and y
#         max_x = max(df_x_list[2*i])
#         max_y = max(df_y_list[2*i])
#         # scale dataset times the ratio
#         df_x_list[2*i] = df_x_list[2*i] / max_x
#         df_y_list[2*i] = df_y_list[2*i] / max_y
#     legend_list_2.append(csv_type_name_list[csv_type_list[i]])
#     legend_list_2.append(csv_type_name_list[0])

# idx_until = -1
# idx_from = 0
# for i in range(len(df_x_list)):
#     ax[1].plot(df_x_list[i][idx_from:idx_until], df_y_list[i][idx_from:idx_until], color=color_list[i], marker='o', markeredgecolor='black')
# ax[1].legend(legend_list_2)
# # plot a green x at 0,0
# ax[1].plot(0, 0, color='green', marker='x', linestyle='none')
# fig.tight_layout(h_pad=2)
# plt.show()