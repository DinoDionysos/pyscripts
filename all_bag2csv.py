import os
from bag2csv_2 import bag2csv_2
from rotate_coor import *

bag2csv_flag = False
# bag2csv_flag = False
# rotate_coor_flag = True
rotate_coor_flag = True

show_plot_for = 2

start_idx = 0
end_idx = 19
indices = range(start_idx, end_idx+1)
# indices = [7,10,12,16,17]

# bag_indices = [9, 15, 28, 19, 17, 51, 49, 34]
bag_indices = [15, 28, 19, 17, 51, 49, 34]
# bag_indices = [9]
# complete list of those who have results
# bag_indices = [9, 14, 15, 16, 17, 19, 21, 28, 29, 33, 34, 46, 47, 48, 49, 50, 51]

folder_orb = "orb"
folder_ssd = "/mnt/d"

##### stuff that do_bag2csv.sh does translated in python
if bag2csv_flag:
    for bag_idx in bag_indices:
        for slam_type in ['stereo','mono', 'd435']:
            folder_ssd = "/mnt/d/"
            file_prefix = "c" + str(bag_idx) + "_" + folder_orb + "_" + slam_type
            folder_orb = folder_orb
            for i in indices:
                bag2csv_2(file_prefix+"_"+str(i), "gt", file_prefix, folder_ssd, folder_orb)
                bag2csv_2(file_prefix+"_"+str(i), "orb", file_prefix, folder_ssd, folder_orb)

if rotate_coor_flag:
    for bag_idx in bag_indices:
        for i in indices:
            shortest_length_csv = -1
            for slam_type in ['mono', 'stereo', 'd435']:
                short_cut_data = folder_orb
                file_prefix = "c" + str(bag_idx) + "_" + folder_orb + "_" + slam_type
                number = str(i)
                path_data = folder_ssd + '/csv/' + folder_orb + '/' + file_prefix + '/' + file_prefix + '_' + number + '-'+short_cut_data+'.csv'
                # get the length of the csv file
                with open(path_data) as f:
                    length_csv = sum(1 for line in f)
                if shortest_length_csv == -1 or length_csv < shortest_length_csv:
                    shortest_length_csv = length_csv
                # print("shortest_length_csv: " + str(shortest_length_csv))
            # now we have the shortest length of all csv files for this scenario with N=number
            for slam_type in ['stereo', 'mono', 'd435']:
                file_prefix = "c" + str(bag_idx) + "_" + folder_orb + "_" + slam_type
                rotate_coor(short_cut_data, str(i), show_plot_for, file_prefix, folder_ssd, folder_orb, shortest_length_csv)
            

# for bag_idx in bag_indices:
#     # for slam_type in ['stereo','mono', 'd435']:
#     for slam_type in ['stereo', 'd435']:
#     # for slam_type in ['mono']: 
#         file_prefix = "c" + str(bag_idx) + "_" + folder_orb + "_" + slam_type 
#         # do do_bag2csv.sh start_idx end_idx file_prefix folder
#         # command = "./do_bag2csv.sh " + str(start_idx) + " " + str(end_idx) + " " + file_prefix + " " + folder + " " + str(show_plot_for)
#         command = "./do_bag2csv.sh " + str(idx) + " " + str(idx) + " " + file_prefix + " " + folder_orb + " " + str(show_plot_for)
#         print(command)
#         #execute command
#         os.system(command)
