import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

show_plot_time = int(sys.argv[3])

# plt.style.use('dark_background')
# plt.rcParams.update({
#     "axes.facecolor": (0.3,0.3,0.3),
#     "figure.facecolor": (0.1,0.1,0.1),
#     "grid.color": (0.3,0.3,0.3)}),
fontsize=14
marker_size=10
linewidth=2
def plot_alignment(trajectroy_true, trajectory_mapped, label1, label2, title, xlabel, ylabel, markeredgecolor, marker, color_error, linewidth=linewidth, marker_size=marker_size, fontsize=fontsize):
    fig = plt.figure()
    plt.axis('equal')
    # plt.title(title, fontsize=fontsize)
    for i in range(len(trajectroy_true)):
        plt.plot([trajectroy_true[i,0], trajectory_mapped[i,0]], [trajectroy_true[i,1], trajectory_mapped[i,1]], color=color_error, linewidth=linewidth)

    plt.plot(trajectroy_true[:,0], trajectroy_true[:,1], marker=marker, markeredgecolor=markeredgecolor, label=label1, linewidth=linewidth, markersize=marker_size)

    plt.plot(trajectory_mapped[:,0], trajectory_mapped[:,1], marker=marker, markeredgecolor=markeredgecolor, label=label2, linewidth=linewidth, markersize=marker_size)

    plt.plot([trajectroy_true[0,0], trajectory_mapped[0,0]], [trajectroy_true[0,1], trajectory_mapped[0,1]], color=color_error, label ="errors") # for label in legend
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    #make lengend with location upper left and make bigger font
    plt.legend(loc=2, prop={'size': fontsize})
    mngr = plt.get_current_fig_manager()
    geom = mngr.window.geometry()
    x,y,dx,dy = geom.getRect()
    mngr.window.setGeometry(pos_fig_x, pos_fig_y, dx, dy)
    return fig

pos_fig_x = 1200
pos_fig_y = 100
folder_name = sys.argv[1].split('/')[2] # f.e. c8_orb_mono

df_gt = pd.read_csv(sys.argv[1])
df_data = pd.read_csv(sys.argv[2])

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
if('mono' in folder_name.split('_')):
    B = np.array([np.array([2,-2]) + c*b for b in mapping_points]) # t + c * R @ # np.array([2,-2])
else:
    B = np.array([t + c * R @ b for b in mapping_points])
mapped_xy = B
# true_points = A




euclidean_distance = np.linalg.norm(mapped_xy - true_points, axis=1)
euclidean_distance_diff = np.diff(euclidean_distance)
euclidean_distance_diff = np.insert(euclidean_distance_diff, 0, 0)
euclidean_distance_diff = euclidean_distance_diff * 1000
euclidean_distance = euclidean_distance * 1000

df_data_time = df_data_time - df_data_time[0]
df_data_timestamp = df_data_timestamp - df_data_timestamp[0]

df_data = pd.DataFrame({'time': df_data_time, 'stamp': df_data_timestamp, 'x': mapped_xy[:,0], 'y': mapped_xy[:,1], 'x_gt': true_points[:,0], 'y_gt': true_points[:,1], 'ape': euclidean_distance, 'rpe': euclidean_distance_diff})

# plot_title = sys.argv[1].split('/')[-1] + ' vs ' + sys.argv[2].split('/')[1]


color_error = 'gray'
label1 = 'ground truth'
label2 = 'vSLAM'
markeredgecolor = 'black'
marker = 'o'
xlabel = 'x [m]'
ylabel = 'y [m]'
every_nth_point = 20
folder_save = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/img/"

fake_translation = np.array([2,-2])
fake_scale = 5

plot_title = 'raw_2'
mapped_xy = np.array([ fake_translation + fake_scale*b for b in mapping_points])
fig = plot_alignment(true_points[::every_nth_point], mapped_xy[::every_nth_point], label1, label2, plot_title, xlabel, ylabel, markeredgecolor, marker, color_error)
plt.savefig(os.path.join(folder_save, 'alignment_' + plot_title + '.pdf'), bbox_inches='tight')
plt.show()

plot_title = 'rotated_2'
mapped_xy = np.array([ fake_translation + fake_scale*R@b for b in mapping_points])
fig = plot_alignment(true_points[::every_nth_point], mapped_xy[::every_nth_point], label1, label2, plot_title, xlabel, ylabel, markeredgecolor, marker, color_error)
plt.savefig(os.path.join(folder_save, 'alignment_' + plot_title + '.pdf'), bbox_inches='tight')
plt.show()

plot_title = 'scaled_2'
mapped_xy = np.array([ fake_translation + c*R@b for b in mapping_points])
fig = plot_alignment(true_points[::every_nth_point], mapped_xy[::every_nth_point], label1, label2, plot_title, xlabel, ylabel, markeredgecolor, marker, color_error)
plt.savefig(os.path.join(folder_save, 'alignment_' + plot_title + '.pdf'), bbox_inches='tight')
plt.show()



plot_title = 'translated_2'
mapped_xy = np.array([ t + c*R@b for b in mapping_points])
fig = plot_alignment(true_points[::every_nth_point], mapped_xy[::every_nth_point], label1, label2, plot_title, xlabel, ylabel, markeredgecolor, marker, color_error)
plt.savefig(os.path.join(folder_save, 'alignment_' + plot_title + '.pdf'), bbox_inches='tight')
plt.show()

# fig = plt.figure()
# plt.axis('equal')
# plt.title(sys.argv[1].split('/')[-1] + ' vs ' + sys.argv[2].split('/')[1])
# for i in range(len(true_points)):
#     plt.plot([true_points[i,0], mapped_xy[i,0]], [true_points[i,1], mapped_xy[i,1]], color='gray')
# plt.plot(true_points[:,0], true_points[:,1], marker='o', markeredgecolor='black', label='true')
# plt.plot(mapped_xy[:,0], mapped_xy[:,1], marker='o', markeredgecolor='black', label='mapped')
# plt.legend()
# mngr = plt.get_current_fig_manager()
# geom = mngr.window.geometry()
# x,y,dx,dy = geom.getRect()
# mngr.window.setGeometry(pos_fig_x, pos_fig_y, dx*2, dy*2)

print('accumulated euclidean distance: ', np.sum(euclidean_distance))
print('accumulated euclidean distance diff: ', np.sum(euclidean_distance_diff))
print('accumulated euclidean distance diff abs: ', np.sum(np.abs(euclidean_distance_diff)))

# csv_file = 'csv/aligned/' + folder_name +'/'+ sys.argv[1].split('/')[-1].split('.')[0]
# csv_file += '_vs_' + sys.argv[2].split('/')[1].split('--')[0] + '.csv'
# if not os.path.exists('csv/aligned/' + folder_name):
#     os.makedirs('csv/aligned/' + folder_name)
# df_data.to_csv(csv_file, index=False)
# print('saved csv to: ' + csv_file)

if show_plot_time > 0:
    plt.show(block=False)
    plt.pause(show_plot_time)
    plt.close(fig)
elif show_plot_time == 0:
    plt.show()

