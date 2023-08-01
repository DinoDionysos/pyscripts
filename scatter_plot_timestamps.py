#!/usr/bin/python3

# %%
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import sys

plt.style.use('dark_background')
plt.rcParams.update({
    "axes.facecolor": (0.5,0.5,0.5),
    "figure.facecolor": (0.1,0.1,0.1),
    "grid.color": (0.3,0.3,0.3)}),

ground_truth_path = sys.argv[1]
camera_pose_path = sys.argv[2]

# read the csv file
df_gt = pd.read_csv(ground_truth_path)
# and the other csv file orbmono
df2 = pd.read_csv(camera_pose_path)

# get the timestamp column
df_timestamp = df_gt['stamp']
# get the timestamp column
df2_timestamp = df2['stamp']
# normalize the timestamp column
df_timestamp = df_timestamp - df_timestamp[0]
# normalize the timestamp column
df2_timestamp = df2_timestamp - df2_timestamp[0]
#convert to numpy array
df_timestamp = df_timestamp.to_numpy()
#convert to numpy array
df2_timestamp = df2_timestamp.to_numpy()
# make arry of ones
ones = np.ones(len(df_timestamp))
# make arry of ones
ones2 = np.ones(len(df2_timestamp))

fig, ax = plt.subplots(2,1)
fig.tight_layout(h_pad=2)

ax[0].set_title('Timestamps')
df_handle = ax[0].plot(df_timestamp, ones, color='blue', marker='o', linestyle='none')
df2_handle = ax[0].plot(df2_timestamp, ones2, color='red', marker='o', linestyle='none') 
ax[0].legend(['Ground Truth', 'ORB SLAM3'])
ax[0].set_xlabel('time')
# hide the y axis
ax[0].axes.get_yaxis().set_visible(False)


# get column x as a numpy array
df_x = df_gt['x'].to_numpy()
# get column y as a numpy array
df_y = df_gt['y'].to_numpy()
# get column x as a numpy array
df2_x = df2['x'].to_numpy()
# get column y as a numpy array
df2_y = df2['y'].to_numpy()
# normalize the x and y columns
df_x = df_x - df_x[0]
df_y = df_y - df_y[0]
# get max value of x and y
max_x = max(df_x)
max_y = max(df_y)
# get max value of x and y
max2_x = max(df2_x)
max2_y = max(df2_y)
# calculate the ratio between the two max values
ratio_x = max_x / max2_x
ratio_y = max_y / max2_y
# scale dataset 2 times the ratio
#df2_x = df2_x * ratio_x
#df2_y = df2_y * ratio_y

ax[1].set_title('Trajectory')
ax[1].plot(df_x, df_y, color='blue', marker='o', linestyle='none')
ax[1].plot(df2_x, df2_y, color='red', marker='o', linestyle='none')
ax[1].legend(['Ground Truth', 'ORB SLAM3'], loc='lower left')
ax[1].set_xlabel('x')
ax[1].set_ylabel('y')

fig.suptitle('ORB SLAM3 vs Ground Truth')
plt.subplots_adjust(top=0.85)
plt.subplots_adjust(hspace=0.6)




plt.show()
