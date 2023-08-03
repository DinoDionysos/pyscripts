import pandas as pd
import sys

# get command line arguments
csv_file = sys.argv[1]

# import the csv file from csv/aligned  
df = pd.read_csv(csv_file)

# calculate the euclidean distance between the ground truth and the data without z
df['euclidean_distance'] = ((df['x_data'] - df['x_gt'])**2 + (df['y_data'] - df['y_gt'])**2)**0.5

#calculate the delta of the euclidean_distance column
df['euclidean_distance_delta'] = df['euclidean_distance'].diff()

#plot histogram of euclidean distance and euclidean distance delta in subplot
import matplotlib.pyplot as plt
fig, ax = plt.subplots(2, 1)
fig.tight_layout(h_pad=2)
ax[0].hist(df['euclidean_distance'], bins=100)
ax[0].set_title('Euclidean Distance')
ax[0].set_xlabel('distance')
ax[1].set_ylabel('count')


ax[1].hist(df['euclidean_distance_delta'], bins=100)
ax[1].set_title('Euclidean Distance Delta')
ax[1].set_xlabel('distance delta')
ax[1].set_ylabel('count')
# plt.show()

#calculate the difference between the x and y columns of the ground truth and the data
df['x_diff'] = df['x_data'] - df['x_gt']
df['y_diff'] = df['y_data'] - df['y_gt']
#plot histogram of x_diff and y_diff in subplot
fig, ax = plt.subplots(2, 1)
fig.tight_layout(h_pad=2)
ax[0].hist(df['x_diff'], bins=100)
ax[0].set_title('X Difference')
ax[0].set_xlabel('x difference')
ax[0].set_ylabel('count')
ax[1].hist(df['y_diff'], bins=100)
ax[1].set_title('Y Difference')
ax[1].set_xlabel('y difference')
ax[1].set_ylabel('count')
# plt.show()

# plot the diffs against the time stamp
fig, ax = plt.subplots(2, 1)
fig.tight_layout(h_pad=2)
ax[0].plot(df['stamp'], df['x_diff'])
ax[0].set_title('X Difference')
ax[0].set_xlabel('time')
ax[0].set_ylabel('x difference')
ax[1].plot(df['stamp'], df['y_diff'])
ax[1].set_title('Y Difference')
ax[1].set_xlabel('time')
ax[1].set_ylabel('y difference')
plt.show()








