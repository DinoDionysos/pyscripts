#!/usr/bin/python3

# %%
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import sys
import os

plt.style.use('dark_background')
plt.rcParams.update({
    "axes.facecolor": (0.5,0.5,0.5),
    "figure.facecolor": (0.1,0.1,0.1),
    "grid.color": (0.3,0.3,0.3)}),

file_name = os.path.basename(__file__)

csv_path_list = []
csv_type_list = []
csv_type_name_list = ['ground_truth', 'mono', 'stereo', 'd435']
# read a dynamic number of input arguments
for i in range(1, len(sys.argv)):
    # if the the argument starts with csv/, then remove it
    if sys.argv[i].startswith('csv/'):
        sys.argv[i] = sys.argv[i].replace('csv/', '')
    # check all the files in csv/ directory if they contain the sys.argv[i] in their name
    # if they do, add them to the csv_path_list
    for file in os.listdir('csv/'):
        if sys.argv[i] in file:
            # if the file is already in the list, do not add it again
            if file in csv_path_list:
                continue
            else:
                csv_path_list.append('csv/'+file)
                #check if the file has ground_truth, mono, stereo or d435 in it and assign a number to csv_type_list accordingly
                if 'ground_truth' in file:  
                    csv_type_list.append(0)
                elif 'mono' in file:
                    csv_type_list.append(1)
                elif 'stereo' in file:
                    csv_type_list.append(2)
                elif 'd435' in file:
                    csv_type_list.append(3)
                else:
                    print("[INFO] "+file_name+" | The file: " + file + " does not contain ground_truth, mono, stereo or d435 in it. Please rename the file accordingly.")
                    sys.exit(1)

df_list = []
for i in range(len(csv_path_list)):
    df_list.append(pd.read_csv(csv_path_list[i]))

# first plot

fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1, 7]})
fig.tight_layout(h_pad=2)
ax[0].set_title('Timestamps')
ax[0].set_xlabel('time')
ax[0].axes.get_yaxis().set_visible(False)
legend_list = []
color_list = ['blue', 'red', 'green', 'orange', 'purple', 'pink', 'cyan', 'yellow']

# for all the csv files in the list
for i in range(len(df_list)):
    # get the timestamp column
    df_timestamp = df_list[i]['stamp']
    # normalize the timestamp column
    df_timestamp = df_timestamp - df_timestamp[0]
    #convert to numpy array
    df_timestamp = df_timestamp.to_numpy()
    # make arry of ones
    ones = np.ones(len(df_timestamp))
    # plot the timestamp
    ax[0].plot(df_timestamp, ones, color=color_list[i], marker='o', linestyle='none')
    legend_list.append(csv_type_name_list[csv_type_list[i]])

ax[0].legend(legend_list)

# second plot
ax[1].set_title('Trajectory')
ax[1].set_xlabel('x')
ax[1].set_ylabel('y')

fig.suptitle('ORB SLAM3 vs Ground Truth')
plt.subplots_adjust(top=0.92)
plt.axis('equal')
# plt.subplots_adjust(hspace=0.6)

df_x_list = []
df_y_list = []
for i in range(len(df_list)):
    df_x_list.append(df_list[i]['x'].to_numpy())
    # df_y_list.append(df_list[i]['y'].to_numpy()) but for d435 we need to use z instead of y
    if csv_type_list[i] == 3:
        df_y_list.append(df_list[i]['z'].to_numpy())
    else:
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
    ax[1].plot(df_x_list[i], df_y_list[i], color=color_list[i], marker='o', markeredgecolor='black') 

# plot a green x at 0,0
ax[1].plot(0, 0, color='green', marker='x', linestyle='none')
ax[1].legend(legend_list)

    

fig.tight_layout(h_pad=2)
plt.show()
