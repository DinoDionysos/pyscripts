import pandas as pd
import sys
import matplotlib.pyplot as plt

plt.rc('axes', axisbelow=True)
fontsize_xlabel = 12
fontsize_ylabel = fontsize_xlabel
labelsize_axes = 11
suptitle = 'ORB stereo vs ground truth' # overall title on the very top

# get command line arguments
csv_file = sys.argv[1]

# import the csv file from csv/aligned  
df = pd.read_csv(csv_file)

# calculate the euclidean distance between the ground truth and the data without z
df['euclidean_distance'] = ((df['x'] - df['x_gt'])**2 + (df['y'] - df['y_gt'])**2)**0.5

#calculate the delta of the euclidean_distance column
df['euclidean_distance_delta'] = df['euclidean_distance'].diff()

#plot histogram of euclidean distance and euclidean distance delta in subplot
fig, ax = plt.subplots(2, 1)
fig.suptitle(suptitle)
ax[0].yaxis.grid(color='gray', linestyle='dashed')
ax[0].hist(df['euclidean_distance'], bins=100)
ax[0].set_title('Euclidean distance')
ax[0].set_xlabel('euclidean distance', fontsize=fontsize_xlabel)
ax[0].set_ylabel('frequency', fontsize=fontsize_ylabel)
ax[1].yaxis.grid(color='gray', linestyle='dashed')
ax[1].hist(df['euclidean_distance_delta'], bins=100)
ax[1].set_title('First discrete difference of euclidean distance')
ax[1].set_xlabel('distance delta', fontsize=fontsize_xlabel)
ax[1].set_ylabel('frequency', fontsize=fontsize_ylabel)
ax[0].tick_params(axis='both', which='major', labelsize=labelsize_axes)
ax[1].tick_params(axis='both', which='major', labelsize=labelsize_axes)


fig.tight_layout(h_pad=2)
# plt.show()

#calculate the difference between the x and y columns of the ground truth and the data
df['x_diff'] = df['x'] - df['x_gt']
df['y_diff'] = df['y'] - df['y_gt']
#plot histogram of x_diff and y_diff in subplot
fig, ax = plt.subplots(2, 1)
fig.suptitle(suptitle)
ax[0].yaxis.grid(color='gray', linestyle='dashed')
ax[0].hist(df['x_diff'], bins=100)
ax[0].set_title('Signed distance to ground truth in x dimension')
ax[0].set_xlabel('distance in x', fontsize=fontsize_xlabel)
ax[0].set_ylabel('frequency', fontsize=fontsize_ylabel)
ax[1].yaxis.grid(color='gray', linestyle='dashed')
ax[1].hist(df['y_diff'], bins=100)
ax[1].set_title('Signed distance to ground truth in y dimension')
ax[1].set_xlabel('distance in y', fontsize=fontsize_xlabel)
ax[1].set_ylabel('frequency', fontsize=fontsize_ylabel)
ax[0].tick_params(axis='both', which='major', labelsize=labelsize_axes)
ax[1].tick_params(axis='both', which='major', labelsize=labelsize_axes)
fig.tight_layout(h_pad=2)
# plt.show()

# plot the diffs against the time stamp
fig, ax = plt.subplots(3, 1)
fig.suptitle(suptitle)
ax[0].yaxis.grid(color='gray', linestyle='dashed')
ax[0].plot(df['stamp'], df['x_diff'])
ax[0].set_title('Signed distance to ground truth in x dimension')
ax[0].set_xlabel('time', fontsize=fontsize_xlabel)
ax[0].set_ylabel('distance in x', fontsize=fontsize_ylabel)
ax[1].yaxis.grid(color='gray', linestyle='dashed')
ax[1].plot(df['stamp'], df['y_diff'])
ax[1].set_title('Signed distance to ground truth in y dimension')
ax[1].set_xlabel('time', fontsize=fontsize_xlabel)
ax[1].set_ylabel('distance in y', fontsize=fontsize_ylabel)
ax[0].tick_params(axis='both', which='major', labelsize=labelsize_axes)
ax[1].tick_params(axis='both', which='major', labelsize=labelsize_axes)
ax[2].yaxis.grid(color='gray', linestyle='dashed')
ax[2].plot(df['stamp'], df['euclidean_distance'])
ax[2].set_title('Euclidean distance to ground truth')
ax[2].set_xlabel('time', fontsize=fontsize_xlabel)
ax[2].set_ylabel('euclidean distance', fontsize=fontsize_ylabel)
ax[2].tick_params(axis='both', which='major', labelsize=labelsize_axes)
# make the figure larger in height
fig.set_figheight(8)


fig.tight_layout(h_pad=1)




plt.show()








