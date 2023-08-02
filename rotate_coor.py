import sys
import pandas as pd
import numpy as np


# load the csv second argument 
df_gt = pd.read_csv(sys.argv[1])
# load the csv for the argument
df_data = pd.read_csv(sys.argv[2])

# get the timestamp column of both dataframes
df_data_timestamp = df_data['stamp']
df_gt_timestamp = df_gt['stamp']
# normalize the timestamp column
df_data_timestamp = df_data_timestamp - df_data_timestamp[0]
df_gt_timestamp = df_gt_timestamp - df_gt_timestamp[0]
#convert to numpy array
df_data_timestamp = df_data_timestamp.to_numpy()
df_gt_timestamp = df_gt_timestamp.to_numpy()

# save the x and y column of the ground truth to numpy array
gt_x = df_gt['x'].to_numpy()
gt_y = df_gt['y'].to_numpy()
# interpolate the data_x and data_y to the length of gt_x and gt_y
gt_x = np.interp(df_data_timestamp, df_gt_timestamp, gt_x)
gt_y = np.interp(df_data_timestamp, df_gt_timestamp, gt_y)
# combine with a zero array as the z column
gt_z = np.zeros(len(gt_x))
# combine into one numpy array
true_points = np.array([gt_x, gt_y, gt_z])

# save the x and y column of the data to numpy array
data_x = df_data['x'].to_numpy()
data_y = df_data['y'].to_numpy()
# zero arry as z column
data_z = np.zeros(len(data_x))
# combine into one numpy array
mapping_points = np.array([data_x, data_y, data_z])

#transpose
true_points = true_points.T
mapping_points = mapping_points.T


# kapsch algorithm from https://stackoverflow.com/questions/60877274/optimal-rotation-in-3d-with-kabsch-algorithm

mapped_centroid = np.average(mapping_points, axis=0)
true_centroid = np.average(true_points, axis=0)

mapping_points -= mapped_centroid
true_points -= true_centroid

h = mapping_points.T @ true_points
u, s, vt = np.linalg.svd(h)
v = vt.T

d = np.linalg.det(v @ u.T)
e = np.array([[1, 0, 0], [0, 1, 0], [0, 0, d]])

r = v @ e @ u.T
tt = true_centroid - np.matmul(r, mapped_centroid)

#mapping
map_list = []
for i in mapping_points:
    point = np.matmul(r, i) + tt
    map_list.append(np.reshape(point, (1, 3)))
mapped_xyz = np.vstack(map_list)

true_points += true_centroid
mapping_points += mapped_centroid
#normalize the such that the first point is 0,0
true_points -= true_points[0]
mapping_points -= mapping_points[0]
mapped_xyz -= mapped_xyz[0]
#plot the x y of mapped_xyz and true_points
import matplotlib.pyplot as plt
# make the scale of x and y equal
plt.axis('equal')
plt.plot(true_points[:,0], true_points[:,1], label='true')
plt.plot(mapped_xyz[:,0], mapped_xyz[:,1], label='mapped')
plt.legend()
plt.show()




# # save the dataframe to the same csv file
# df.to_csv(sys.argv[1], index=False)

# save to differnet csv file
df_data.to_csv('csv/rotated_stereo.csv', index=False)
