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

pos_fig_x = 1200
pos_fig_y = 100
folder_name = sys.argv[1].split('/')[2]

df_gt = pd.read_csv(sys.argv[1])
df_data = pd.read_csv(sys.argv[2])

df_data_timestamp = df_data['stamp']
df_gt_timestamp = df_gt['stamp']
df_data_timestamp = df_data_timestamp - df_data_timestamp[0]
df_gt_timestamp = df_gt_timestamp - df_gt_timestamp[0]
df_data_timestamp = df_data_timestamp.to_numpy()
df_gt_timestamp = df_gt_timestamp.to_numpy()

# prepare true_points and mapping_points arrays for kabsch algorithm
gt_x = df_gt['x'].to_numpy()
gt_y = df_gt['y'].to_numpy()
gt_x = np.interp(df_data_timestamp, df_gt_timestamp, gt_x)
gt_y = np.interp(df_data_timestamp, df_gt_timestamp, gt_y)
gt_z = np.zeros(len(gt_x))
true_points = np.array([gt_x, gt_y, gt_z])

data_x = df_data['x'].to_numpy()
# if sys.arg[2] contains orb and d435 and not imu then get the z axis instead of the y axis
if 'orb' in sys.argv[2] and 'd435' in sys.argv[2] and 'imu' not in sys.argv[2]:
    data_y = df_data['z'].to_numpy()
else:
    data_y = df_data['y'].to_numpy()
data_z = np.zeros(len(data_x))
mapping_points = np.array([data_x, data_y, data_z])

true_points = true_points.T
mapping_points = mapping_points.T
# kabsch algorithm from https://stackoverflow.com/questions/60877274/optimal-rotation-in-3d-with-kabsch-algorithm
# as far as I understand it resembles the horn method implementations that I have seen like ein horn_demo.py. The difference seems laut wikipedia that horn is in qaternion and kabsch is in rotation matrix.
#For an alternative kabsch implementation see here https://zpl.fi/aligning-point-patterns-with-kabsch-umeyama-algorithm/
mapped_centroid = np.average(mapping_points, axis=0)
true_centroid = np.average(true_points, axis=0)
mapping_points -= mapped_centroid
true_points -= true_centroid
h = mapping_points.T @ true_points
u, s, vt = np.linalg.svd(h)
v = vt.T
d = np.linalg.det(v @ u.T)
# get the sign of d
# solution from stackoverflow does not implement the sign here? wikipedia says it should be and the horn_demo.py also does it.
# https://en.wikipedia.org/wiki/Kabsch_algorithm
d = np.sign(d) 
e = np.array([[1, 0, 0], [0, 1, 0], [0, 0, d]])
r = v @ e @ u.T
tt = true_centroid - np.matmul(r, mapped_centroid)
true_points += true_centroid
mapping_points += mapped_centroid

#mapping
map_list = []
for i in mapping_points:
    point = np.matmul(r, i) + tt
    map_list.append(np.reshape(point, (1, 3)))
mapped_xyz = np.vstack(map_list)

# normalize such that the first point is 0,0
# true_points -= true_points[0]
# mapping_points -= mapping_points[0]
# mapped_xyz -= mapped_xyz[0]

euclidean_distance = np.linalg.norm(mapped_xyz - true_points, axis=1)
euclidean_distance_diff = np.diff(euclidean_distance)
euclidean_distance_diff = np.insert(euclidean_distance_diff, 0, 0)
euclidean_distance_diff = euclidean_distance_diff * 1000
euclidean_distance = euclidean_distance * 1000
df_data = pd.DataFrame({'stamp': df_data_timestamp, 'x': mapped_xyz[:,0], 'y': mapped_xyz[:,1], 'x_gt': true_points[:,0], 'y_gt': true_points[:,1], 'dist': euclidean_distance, 'ffd': euclidean_distance_diff})

fig = plt.figure()
plt.axis('equal')
plt.title(sys.argv[1].split('/')[-1] + ' vs ' + sys.argv[2].split('/')[1])
for i in range(len(true_points)):
    plt.plot([true_points[i,0], mapped_xyz[i,0]], [true_points[i,1], mapped_xyz[i,1]], color='gray')
plt.plot(true_points[:,0], true_points[:,1], marker='o', markeredgecolor='black', label='true')
plt.plot(mapped_xyz[:,0], mapped_xyz[:,1], marker='o', markeredgecolor='black', label='mapped')
plt.legend()
mngr = plt.get_current_fig_manager()
geom = mngr.window.geometry()
x,y,dx,dy = geom.getRect()
mngr.window.setGeometry(pos_fig_x, pos_fig_y, dx*2, dy*2)

print('accumulated euclidean distance: ', np.sum(euclidean_distance))
print('accumulated euclidean distance diff: ', np.sum(euclidean_distance_diff))
print('accumulated euclidean distance diff abs: ', np.sum(np.abs(euclidean_distance_diff)))

csv_file = 'csv/aligned/' + folder_name +'/'+ sys.argv[1].split('/')[-1].split('.')[0]
csv_file += '_vs_' + sys.argv[2].split('/')[1].split('--')[0] + '.csv'
if not os.path.exists('csv/aligned/' + folder_name):
    os.makedirs('csv/aligned/' + folder_name)
df_data.to_csv(csv_file, index=False)
print('saved csv to: ' + csv_file)

plt.show(block=False)
plt.pause(5)
plt.close(fig)





