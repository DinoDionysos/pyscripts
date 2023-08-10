import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('dark_background')
plt.rcParams.update({
    "axes.facecolor": (0.3,0.3,0.3),
    "figure.facecolor": (0.1,0.1,0.1),
    "grid.color": (0.3,0.3,0.3)}),

folder_name = sys.argv[1].split('/')[2]
print(folder_name) 

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
# if sys.arg[2] contains orb and d435 and not imu then get the z axis instead of the y axis
if 'orb' in sys.argv[2] and 'd435' in sys.argv[2] and 'imu' not in sys.argv[2]:
    data_y = df_data['z'].to_numpy()
else:
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

# calculate the euclidean distance between the mapped_xyz and true_points
euclidean_distance = np.linalg.norm(mapped_xyz - true_points, axis=1)
# calculate the diff of the euclidean distance
euclidean_distance_diff = np.diff(euclidean_distance)
# append a zero to the euclidean_distance_diff at the front
euclidean_distance_diff = np.insert(euclidean_distance_diff, 0, 0)
# *1000
euclidean_distance_diff = euclidean_distance_diff * 1000
euclidean_distance = euclidean_distance * 1000
# make a dataframe from the mapped_xyz, true_points and timestamps and euclidean_distance and euclidean_distance_diff
df_data = pd.DataFrame({'stamp': df_data_timestamp, 'x': mapped_xyz[:,0], 'y': mapped_xyz[:,1], 'x_gt': true_points[:,0], 'y_gt': true_points[:,1], 'dist': euclidean_distance, 'ffd': euclidean_distance_diff})


# split the argument 1 by '/' and get the last part
csv_file = 'csv/aligned/' + folder_name +'/'+ sys.argv[1].split('/')[-1].split('.')[0]
csv_file += '_vs_' + sys.argv[2].split('/')[1].split('--')[0] + '.csv'
# csv_file += '_vs_' + sys.argv[2].split('/')[1]
# csv_file += '_vs_' + sys.argv[2].split('/')[1]
# csv_file += '_vs_' + sys.argv[2].split('/')[1]
# save the dataframe as csv
# if folder_name does not exist create it
if not os.path.exists('csv/aligned/' + folder_name):
    os.makedirs('csv/aligned/' + folder_name)
print(csv_file)
df_data.to_csv(csv_file, index=False)

# plot the x y of mapped_xyz and true_points
# make the scale of x and y equal
plt.axis('equal')
# for all points with the same timestamp plot a line between them
for i in range(len(true_points)):
    plt.plot([true_points[i,0], mapped_xyz[i,0]], [true_points[i,1], mapped_xyz[i,1]], color='gray')
plt.plot(true_points[:,0], true_points[:,1], marker='o', markeredgecolor='black', label='true')
plt.plot(mapped_xyz[:,0], mapped_xyz[:,1], marker='o', markeredgecolor='black', label='mapped')

plt.legend()
plt.show()





