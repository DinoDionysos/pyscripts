#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os

# 1: bag name (withouth .bag)
# 2: topic name or shortcut (gt or orb)
# 3: folder_prefix (c8_orb_mono)
# 4: path to external ssd folder (/mnt/d)
# 5: folder orb (orb)


bag_name_with_number_without_extension = sys.argv[1] #c8_orb_mono_1
topic_name = sys.argv[2] # gt or orb oder sonst was
folder_prefix = sys.argv[3] # c8_orb_mono
path_external_ssd = sys.argv[4] # /mnt/d
folder_orb = sys.argv[5] # orb


folder_rosbags = path_external_ssd+"/rosbags/"+ folder_orb +"/"+folder_prefix # /mnt/d/rosbags/orb/c8_orb_mono
bag_name = bag_name_with_number_without_extension + ".bag" # c8_orb_mono_1.bag
bag_path = folder_rosbags+"/"+bag_name # /mnt/d/rosbags/c8_orb_mono/c8_orb_mono_1.bag

topic_name_str = topic_name
if topic_name == 'gt':
    topic_name = '/ground_truth/odom'
elif topic_name == 'orb':
    topic_name = '/orb_slam3/camera_pose'
# get the name of the file that we are executing
file_name = os.path.basename(__file__)
# check if the user has provided the correct number of arguments
# if len(sys.argv) > 4 or len(sys.argv) < 3:
#     print("[INFO] "+file_name+" | Usage: python3 "+file_name+" <bag_name> <topic_name> optional:<topic_type> \nThe file <bag_name> should be placed in the bags folder respectively. \nIt is not necessary to have 'bags/' in the beginning of the <bag_name>.\n <topic_type> is optional and can be found by executing: 'rosbag info <bag_name> -y -k topics'\n <topic_name> has a '/' in the beginning.")
#     sys.exit(1)

# if bag_name.startswith('bags/'):
#     bag_name = bag_name.replace('bags/', '')

# folder_name = bag_name.split('/')[0] +'/'+bag_name.split('/')[1]



# print("[INFO] "+file_name+" | search for topic type of topic: " + topic_name + " in bag: " + bag_name)
# if len(sys.argv) == 4:
#     topic_type = sys.argv[3]
# else:
output = os.popen('rosbag info '+bag_path+' -y -k topics').read()
# split the output. an entry begins with '-'
output = output.split('-')
# remove the first entry because it is empty
output.pop(0)
# search for the topic type in the output
topic_type = ""
for cell in output:
    # get the word between "topic:" and "\n"
    candiate = cell.split('topic: ')[1].split('\n')[0]
    # compare the candidate with the topic_name
    if candiate == topic_name:
        # print("[INFO] "+file_name+" | found topic name in bag info: " + topic_name)
        # get the word between "type:" and "\n"
        topic_type = cell.split('type: ')[1].split('\n')[0]
        # print("[INFO] "+file_name+" | found topic type: " + topic_type)

if topic_type == "":
    print("[INFO] "+file_name+" | The topic type could not be resolved from the topic name: " + topic_name + " and the bag: " + bag_name + ".\nPlease provide the topic type as the third argument. f.e. nav_msgs/Odometry")
    sys.exit(1)

# print("[INFO] "+file_name+" | done with search for topic type of topic: " + topic_name + " in bag: " + bag_name)
# make csv_file the combination of first and second
csv_file = bag_name_with_number_without_extension + '-' + topic_name_str  + '.csv'

csv_folder = path_external_ssd + "/csv/" + folder_orb +'/'+ folder_prefix
csv_path = csv_folder + "/" + csv_file

if not os.path.exists(csv_folder):
    os.makedirs(csv_folder)
    print("[INFO] "+file_name+" | created folder: " + csv_folder)

command = 'rostopic echo -b '+bag_path+' -p '+topic_name+' > '+csv_path
print("[INFO] "+file_name+" | executing: " + command)
os.system(command)
# print("[INFO] "+file_name+" | done executing: " + command)

df = pd.read_csv(csv_path)


# drop the all columns with twist in the name
df = df[df.columns.drop(list(df.filter(regex='twist')))]
df = df[df.columns.drop(list(df.filter(regex='covariance')))]
df = df[df.columns.drop(list(df.filter(regex='frame_id')))]
# remove the "field." from the column names
df.columns = df.columns.str.replace('field.', '')
df.columns = df.columns.str.replace('pose.', '')
df.columns = df.columns.str.replace('position.', '')
df.columns = df.columns.str.replace('orientation.', 'quat_')
df.columns = df.columns.str.replace('%', '')
df.columns = df.columns.str.replace('header.', '')

#order the rows with respect to the stamp
df = df.sort_values(by=['stamp'])
# if a row has the same stamp as the row before, drop it
df = df.drop_duplicates(subset=['stamp'], keep='first')


# reset the index
df = df.reset_index(drop=True)



df.to_csv(csv_path, index=False)
# print("[INFO] "+file_name+" | saved to: " + csv_file)




