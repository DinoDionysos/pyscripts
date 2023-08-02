import sys
import pandas as pd
import numpy as np

# load the csv for the argument
df_data = pd.read_csv(sys.argv[1])
# load the csv second argument 
df_gt = pd.read_csv(sys.argv[2])

# get the timestamp column of both dataframes
df_data_timestamp = df_data['stamp']
df_gt_timestamp = df_gt['stamp']
# normalize the timestamp column
df_data_timestamp = df_data_timestamp - df_data_timestamp[0]
df_gt_timestamp = df_gt_timestamp - df_gt_timestamp[0]
#convert to numpy array
df_data_timestamp = df_data_timestamp.to_numpy()
df_gt_timestamp = df_gt_timestamp.to_numpy()

# save the x and y column of the ground truth and data to numpy array
gt_x = df_gt['x'].to_numpy()
gt_y = df_gt['y'].to_numpy()
data_x = df_data['x'].to_numpy()
data_y = df_data['y'].to_numpy()

# print data_x and data_y the first 10 elements
print(data_x[:10])
print(data_y[:10])
# print length of data_x and data_y
print(len(data_x))
print(len(data_y))

# interpolate the data_x and data_y to the length of gt_x and gt_y
data_x = np.interp(df_gt_timestamp, df_data_timestamp, data_x)
data_y = np.interp(df_gt_timestamp, df_data_timestamp, data_y)

# print data_x and data_y
print(data_x[:10])
print(data_y[:10])
# print length of data_x and data_y
print(len(data_x))
print(len(data_y))


# plot them in the same figure
import matplotlib.pyplot as plt
plt.plot(gt_x, gt_y, label='ground truth')
plt.plot(data_x, data_y, label='data')
plt.legend()
plt.show()


