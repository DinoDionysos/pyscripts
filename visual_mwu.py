import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from util_error_measures import *

folders = ["csv/aligned/c8_orb_stereo", "csv/aligned/c8_orb_d435", "csv/aligned/c8_orb_mono"]
folder_save = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/img/"
# list of length #folders of lists of length N with array with #(poses in traj) ape elements
list_slam_repet_trajec_ape = [read_cols_from_folder(folder, "ape") for folder in folders] 
names_of_slams = ['stereo', 'RGBD', 'mono']

stereo = list_slam_repet_trajec_ape[0][0]
rgbd = list_slam_repet_trajec_ape[1][0]

# tell shape or length
print(np.shape(stereo))
print(np.shape(rgbd))

# sort both arrays
stereo.sort()
rgbd.sort()



count_list_smaller = []
# compare every element of stereo with every element of rgbd and count if stereo is smaller
for i in range(0, len(stereo)):
    count = 0
    for j in range(0, len(rgbd)):
        if(stereo[i] < rgbd[j]):
            count = count + 1
    count_list_smaller.append(count)

# do the same but count if stereo is bigger
count_list_bigger = []
for i in range(0, len(stereo)):
    count = 0
    for j in range(0, len(rgbd)):
        if(stereo[i] >= rgbd[j]):
            count = count + 1
    count_list_bigger.append(count)

# check if the are equal if you add them up
check_list_added = []
for i in range(0, len(check_list_added)):
    check_list_added.append(check_list_added[i] + count_list_bigger[i])

#check if every element is equal to len(rgbd)
for i in range(0, len(check_list_added)):
    if(check_list_added[i] != len(rgbd)):
        # print len rgbd and check_list_added[i]
        print("len(rgbd): ", len(rgbd), "check_list_added[i]: ", check_list_added[i])
    else:
        print("len(rgbd): ", len(rgbd), "check_list_added[i]: ", check_list_added[i], "count_list_smaller[i]: ", count_list_smaller[i], "count_list_bigger[i]: ", count_list_bigger[i])

# make anumpy array with dimensions len(stereo) x len(rgbd) and fill it with zeros
count_array = np.zeros((len(rgbd),len(stereo)))
for i in range(0, len(stereo)):
    for j in range(0, count_list_bigger[i]):
        count_array[j][i] = 1

# plot it in color green and red
# give a cmap with two different colors
cmap = plt.cm.get_cmap('RdYlGn')
plt.imshow(count_array, cmap=cmap, vmin=0, vmax=1)
fontsize= 12
# xlabel
plt.xlabel("index of ordered elements in dataset 1", fontsize=fontsize)
# ylabel
plt.ylabel("index of ordered elements in dataset 2", fontsize=fontsize)
# axis tick font size
plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)

# new list with every element len rgbd - count_list_smaller[i]
count_list_smaller_new = []
for i in range(0, len(count_list_smaller)):
    count_list_smaller_new.append(len(rgbd) - count_list_smaller[i])
# plt.plot(count_list_smaller_new, color='black')
plt.plot(count_list_bigger, color='white')
# make list that has its index as element
count_list_index = []
for i in range(0, len(count_list_smaller)):
    count_list_index.append((i/len(stereo)*len(rgbd)))
plt.plot(count_list_index, color='black')
# add text to upper left corner
space_red = 250
plt.text( space_red, len(rgbd)-space_red, "red area: U of dataset 2", fontsize=fontsize)
# add text to lower right corner
space_green = 150
plt.text(len(stereo)-700, space_green, "green area: U of dataset 1", fontsize=fontsize)
# flip the ticks of the y axis without flipping the plot
plt.gca().invert_yaxis()
plt.savefig(folder_save + "mwu_visualization.pdf")
plt.show()



