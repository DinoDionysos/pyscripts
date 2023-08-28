import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.spatial.transform import Rotation
from scipy.spatial.transform import Slerp



show_plot_time = int(sys.argv[3])

# plt.style.use('dark_background')
# plt.rcParams.update({
#     "axes.facecolor": (0.3,0.3,0.3),
#     "figure.facecolor": (0.1,0.1,0.1),
#     "grid.color": (0.3,0.3,0.3)}),

pos_fig_x = 1200
pos_fig_y = 100
folder_name = sys.argv[1].split('/')[2] # f.e. c8_orb_mono

divide_time = 1000000

df_gt = pd.read_csv(sys.argv[1])
df_data = pd.read_csv(sys.argv[2])

# shift both timestamps with df_data_timestamp[0]. This is just a normalization for df_data and a shift for df_gt!
# devide by 1000000
df_data_timestamp = df_data['stamp'].to_numpy()
df_gt_timestamp = df_gt['stamp'].to_numpy()


# cut the timestamps that are smaller than the beginning of the gt
df_data = df_data[df_data['stamp'] >= df_gt_timestamp[0]]
df_data = df_data[df_data['stamp'] <= df_gt_timestamp[-1]]
df_data = df_data.reset_index(drop=True)

df_data_timestamp = df_data['stamp'].to_numpy()
df_gt_timestamp = df_gt['stamp'].to_numpy()
df_data_time = df_data['time'].to_numpy()
df_gt_time = df_gt['time'].to_numpy()
# do not normalize the time before interpolation!
df_gt['seq'] = df_gt['seq'] - df_gt['seq'][0]
df_gt['x'] = df_gt['x'] - df_gt['x'][0]
df_gt['y'] = df_gt['y'] - df_gt['y'][0]
df_gt['z'] = df_gt['z'] - df_gt['z'][0]
df_data['seq'] = df_data['seq'] - df_data['seq'][0]
df_data['x'] = df_data['x'] - df_data['x'][0]
df_data['y'] = df_data['y'] - df_data['y'][0]
df_data['z'] = df_data['z'] - df_data['z'][0]
#shift both timestamps with df_data_timestamp[0]. This is just a normalization for df_data and a shift for df_gt!
import copy
shift_by = copy.deepcopy(df_data_timestamp[0])
df_data_timestamp = df_data_timestamp - shift_by
df_gt_timestamp = df_gt_timestamp - shift_by
# devide
df_data_timestamp = df_data_timestamp / divide_time
df_gt_timestamp = df_gt_timestamp / divide_time
print('shifted by: ', shift_by)
# [0] print
print('df_data_timestamp[0]: ', df_data_timestamp[0])
print('df_gt_timestamp[0]: ', df_gt_timestamp[0])
print('df_data_timestamp[-1]: ', df_data_timestamp[-1])
print('df_gt_timestamp[-1]: ', df_gt_timestamp[-1])



def get_rotations_from_quaternions(df : pd.DataFrame, d435=False):
    # use a multidimensional array to store the rotations
    list_of_quat = []
    for i in range(len(df)):
        if d435:
            q = np.array([df.loc[i, 'quat_x'], df.loc[i, 'quat_z'], df.loc[i, 'quat_y'], df.loc[i, 'quat_w']])
        else:
            q = np.array([df.loc[i, 'quat_x'], df.loc[i, 'quat_y'], df.loc[i, 'quat_z'], df.loc[i, 'quat_w']])
        list_of_quat.append(q)
    list_of_rotations = Rotation.from_quat(list_of_quat)
    return list_of_rotations

    #get the list of rotations from the data and gt
if 'orb' in sys.argv[2] and 'd435' in sys.argv[2]:
    list_of_rotations_data = get_rotations_from_quaternions(df_data, d435=True)
else:
    list_of_rotations_data = get_rotations_from_quaternions(df_data)
list_of_rotations_gt = get_rotations_from_quaternions(df_gt)
#create slerp object with timestamp of gt and list of rotations of gt
slerp = Slerp(df_gt_timestamp, list_of_rotations_gt)
#interpolate the rotations of gt at the timestamps of data
list_of_rotations_gt = slerp(df_data_timestamp)
# get the euler from the list of rotations
euler_gt = np.array([r.as_euler('xyz', degrees=True) for r in list_of_rotations_gt])
# get the euler from the list of rotations
euler_data = np.array([r.as_euler('xyz', degrees=True) for r in list_of_rotations_data])
# make single arrays for roll pitch yaw
roll_gt = euler_gt[:,0]
pitch_gt = euler_gt[:,1]
yaw_gt = euler_gt[:,2]
roll = euler_data[:,0]
pitch = euler_data[:,1]
if 'orb' in sys.argv[2] and 'd435' in sys.argv[2]:
    yaw = euler_data[:,2] * (-1)
else:
    yaw = euler_data[:,2]


# normalize the euler
roll = roll - roll[0]
pitch = pitch - pitch[0]
yaw = yaw - yaw[0]
roll_gt = roll_gt - roll_gt[0]
pitch_gt = pitch_gt - pitch_gt[0]
yaw_gt = yaw_gt - yaw_gt[0]
# correct the euler that are over 180 degrees and under -180 degrees
for i in range(len(roll)):
    if roll[i] > 180:
        roll[i] = roll[i] - 360
    elif roll[i] < -180:
        roll[i] = roll[i] + 360
    if pitch[i] > 180:
        pitch[i] = pitch[i] - 360
    elif pitch[i] < -180:
        pitch[i] = pitch[i] + 360
    if yaw[i] > 180:
        yaw[i] = yaw[i] - 360
    elif yaw[i] < -180:
        yaw[i] = yaw[i] + 360
for i in range(len(roll_gt)):
    if roll_gt[i] > 180:
        roll_gt[i] = roll_gt[i] - 360
    elif roll_gt[i] < -180:
        roll_gt[i] = roll_gt[i] + 360
    if pitch_gt[i] > 180:
        pitch_gt[i] = pitch_gt[i] - 360
    elif pitch_gt[i] < -180:
        pitch_gt[i] = pitch_gt[i] + 360
    if yaw_gt[i] > 180:
        yaw_gt[i] = yaw_gt[i] - 360
    elif yaw_gt[i] < -180:
        yaw_gt[i] = yaw_gt[i] + 360





        


# prepare true_points and mapping_points arrays for kabsch algorithm
gt_x = df_gt['x'].to_numpy()
gt_y = df_gt['y'].to_numpy()
gt_x = np.interp(df_data_timestamp, df_gt_timestamp, gt_x)
gt_y = np.interp(df_data_timestamp, df_gt_timestamp, gt_y)
true_points = np.array([gt_x, gt_y])

data_x = df_data['x'].to_numpy()
if 'orb' in sys.argv[2] and 'd435' in sys.argv[2] and 'imu' not in sys.argv[2]:
    data_y = df_data['z'].to_numpy()
else:
    data_y = df_data['y'].to_numpy()
mapping_points = np.array([data_x, data_y])
true_points = true_points.T
mapping_points = mapping_points.T

# source:https://zpl.fi/aligning-point-patterns-with-kabsch-umeyama-algorithm/
# take only the first from true_points points from 50 to 100 for A and B
A = true_points
B = mapping_points
n, m = A.shape
EA = np.mean(A, axis=0)
EB = np.mean(B, axis=0)
VarA = np.mean(np.linalg.norm(A - EA, axis=1) ** 2)
H = ((A - EA).T @ (B - EB)) / n
U, D, VT = np.linalg.svd(H)
d = np.sign(np.linalg.det(U) * np.linalg.det(VT))
S = np.diag([1] * (m - 1) + [d])
R = U @ S @ VT
c = VarA / np.trace(np.diag(D) @ S)
t = EA - c * R @ EB
B = np.array([t + c * R @ b for b in B])
# if('mono' in folder_name.split('_')):
#     B = np.array([t + c * R @ b for b in mapping_points])
# else:
#     B = np.array([t + c * R @ b for b in mapping_points])
mapped_xy = B
# true_points = A

# mapped_xy = mapped_xy - mapped_xy[0]
# true_points = true_points - true_points[0]


xy_ape = np.linalg.norm(mapped_xy - true_points, axis=1)
xy_rpe = np.diff(xy_ape)
xy_rpe = np.insert(xy_rpe, 0, 0)
xy_rpe = xy_rpe * 1000
xy_ape = xy_ape * 1000

yaw_ape = abs(yaw - yaw_gt)
for i in range(len(yaw_ape)): #correction for -180 180 step
    if yaw_ape[i] > 180:
        yaw_ape[i] = yaw_ape[i] - 360
    elif yaw_ape[i] < -180:
        yaw_ape[i] = yaw_ape[i] + 360
yaw_rpe = np.diff(yaw_ape)
yaw_rpe = np.insert(yaw_rpe, 0, 0)

#print max and min of yaw_diff
print('yaw_diff max: ', np.max(yaw_ape))
print('yaw_diff min: ', np.min(yaw_ape))

df_data_time = df_data_time - df_data_time[0]
df_data_timestamp = df_data_timestamp - df_data_timestamp[0]

df_data = pd.DataFrame({'seq': df_data['seq'].to_numpy(),
                        'time': df_data_time,
                        'stamp': df_data_timestamp,
                        'x': mapped_xy[:,0],
                        'y': mapped_xy[:,1],
                        'x_gt': true_points[:,0],
                        'y_gt': true_points[:,1],
                        'xy_ape': xy_ape,
                        'xy_rpe': xy_rpe,
                        'yaw': yaw,
                        'yaw_gt': yaw_gt,
                        'yaw_ape': yaw_ape,
                        'yaw_rpe': yaw_rpe,
                        'seq2': df_data['seq'].to_numpy(),
                        # 'pitch': pitch,
                        # 'pitch_gt': pitch_gt,
                        # 'roll': roll,
                        # 'roll_gt': roll_gt,
                        })

fig = plt.figure()
plt.axis('equal')
plt.title(sys.argv[1].split('/')[-1] + ' vs ' + sys.argv[2].split('/')[1])
for i in range(len(true_points)):
    plt.plot([true_points[i,0], mapped_xy[i,0]], [true_points[i,1], mapped_xy[i,1]], color='gray')
plt.plot(true_points[:,0], true_points[:,1], marker='o', markeredgecolor='black', label='true')
plt.plot(mapped_xy[:,0], mapped_xy[:,1], marker='o', markeredgecolor='black', label='mapped')
plt.legend()
mngr = plt.get_current_fig_manager()
geom = mngr.window.geometry()
x,y,dx,dy = geom.getRect()
mngr.window.setGeometry(pos_fig_x, pos_fig_y, dx*2, dy*2)

print('accumulated euclidean distance: ', np.sum(xy_ape))
print('accumulated euclidean distance diff: ', np.sum(xy_rpe))
print('accumulated euclidean distance diff abs: ', np.sum(np.abs(xy_rpe)))

csv_file = 'csv/aligned/' + folder_name +'/'+ sys.argv[1].split('/')[-1].split('.')[0]
csv_file += '_vs_' + sys.argv[2].split('/')[1].split('--')[0] + '.csv'
if not os.path.exists('csv/aligned/' + folder_name):
    os.makedirs('csv/aligned/' + folder_name)
df_data.to_csv(csv_file, index=False)
print('saved csv to: ' + csv_file)

if show_plot_time > 0:
    plt.show(block=False)
    plt.pause(show_plot_time)
    plt.close(fig)
elif show_plot_time == 0:
    pass
else:
    plt.show()






def interpolate_360(x_eval, x_data, y_data):
    y_eval = []
    for i in range(0, len(x_eval)):
        # get the index of the closest value in x_data to x_eval[i]
        index1 = np.argmin(np.abs(x_data - x_eval[i]))
        # if x_data[i]-x_eval[i] is negative, the value in x_data[i] is smaller than x_eval[i], then take i+1 as index2
        if x_data[index1] - x_eval[i] < 0:
            index2 = index1 + 1
        else:
            index2 = index1 - 1
        # if index2 is out of range, set it to index
        if index2 < 0 or index2 > len(x_data)-1:
            index2 = index1
        # get the value of the closest index
        y1 = y_data[index1]
        y2 = y_data[index2]
        # get the difference of y2 and y1
        y_diff = y2 - y1
        if y_diff > 270:
            y1 = y1 + 360
        if y_diff < -270:
            y2 = y2 + 360

        x1 = x_data[index1]
        x2 = x_data[index2]
        # get the difference of x2 and x1
        x_diff = x2 - x1
        x_int = x_eval[i]
        # interpolate y_int at x_int
        y_int = y1 + (y2 - y1 / x_diff) * (x_int - x1)

        if y_int > 360:
            y_int = y_int % 360
        if y_int < 0:
            y_int = y_int + 360
        y_eval.append(y_int)
    return np.array(y_eval)


# testing to get the rotation from R
# print(R)
# # get arccos of the first element of the first row of R and the last element of the last row of R
# print(np.arccos(R[0,0]) * 180 / np.pi)
# print(np.arccos(R[1,1]) * 180 / np.pi)
# # get the arc sin of the second element of the first row of R
# print(np.arcsin(R[0,1]) * 180 / np.pi)
# print(np.arcsin(R[1,0]) * 180 / np.pi)
# # get the angle of the rotation matrix
# print(np.arctan2(R[1,0], R[0,0]) * 180 / np.pi)
# print(np.arctan2(R[1,1], R[0,1]) * 180 / np.pi)
# # testing delete me delete me
# # make R eye matrix
# # R = np.eye(2)
# deg_arccos = (np.arccos(R[0,0]) * 180 / np.pi)
# deg_arcsin = (np.arcsin(R[0,1]) * 180 / np.pi)
# deg_arcsin_ = (np.arcsin(R[1,0]) * 180 / np.pi)
# deg_arctan = (np.arctan2(R[1,0], R[0,0]) * 180 / np.pi)
# deg_arctan_ = (np.arctan2(R[1,1], R[0,1]) * 180 / np.pi)
# # make R rotation matrix with deg_arccos degree
# # R = np.array([[np.cos(deg_arccos), -np.sin(deg_arccos)], [np.sin(deg_arccos), np.cos(deg_arccos)]])
# # make R rotation matrix with deg_arcsin degree
# # R = np.array([[np.cos(deg_arcsin), -np.sin(deg_arcsin)], [np.sin(deg_arcsin), np.cos(deg_arcsin)]])
# # make R rotation matrix with deg_arcsin_ degree
# # R = np.array([[np.cos(deg_arcsin_), -np.sin(deg_arcsin_)], [np.sin(deg_arcsin_), np.cos(deg_arcsin_)]])
# # make R rotation matrix with deg_arctan degree
# # R = np.array([[np.cos(deg_arctan), -np.sin(deg_arctan)], [np.sin(deg_arctan), np.cos(deg_arctan)]])
# # make R rotation matrix with deg_arctan_ degree
# # R = np.array([[np.cos(deg_arctan_), -np.sin(deg_arctan_)], [np.sin(deg_arctan_), np.cos(deg_arctan_)]])
