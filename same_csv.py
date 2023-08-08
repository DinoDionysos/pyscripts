# compare if csv/c4_d1_d435_orb-bag--orb_slam3-camera_pose.csv and csv/orb-d1_d435_orb_c4-bag--orb_slam3-camera_pose.csv are the same

import pandas as pd
import sys

# # replace d1 with d2 for both argv
# sys.argv[1] = sys.argv[1].replace('d1', 'd2')
# sys.argv[2] = sys.argv[2].replace('d1', 'd2')

df1 = pd.read_csv(sys.argv[1])
df2 = pd.read_csv(sys.argv[2])

#compare the two dataframes and give boolean if same or not
print(df1.equals(df2))
 #print names of the csv files
print(sys.argv[1])
print(sys.argv[2])

# if they are not the same, print the differences
if not df1.equals(df2):
    print(df1.compare(df2))
    

