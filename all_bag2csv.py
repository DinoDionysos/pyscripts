import os

folder = "orb"
start_idx = 0
end_idx = 19
show_plot_for = 2
# bag_indices = [14, 15, 16, 17, 19, 21, 32, 28, 33, 34]#, 32, 27, 29]
# bag_indices = [36,37,27,29,23,24]
bag_indices = [34]#, 29, 33, 34]#, 14, 15, 16, 17, 19, 21, 32, 27, 28, 29, 33, 34]
#  32 mono und d435 is noch nicht gefahren
# 27 d435 nicht gefahren

for bag_idx in bag_indices:
    for slam_type in ['stereo','mono', 'd435']: #, 
        file_prefix = "c" + str(bag_idx) + "_" + folder + "_" + slam_type 
        # do do_bag2csv.sh start_idx end_idx file_prefix folder
        command = "./do_bag2csv.sh " + str(start_idx) + " " + str(end_idx) + " " + file_prefix + " " + folder + " " + str(show_plot_for)
        print(command)
        #execute command
        os.system(command)
