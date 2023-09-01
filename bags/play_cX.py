import os
import sys
path=sys.argv[1]
folder_rosbags = path
short_cut = sys.argv[2]
#get all the folders in the path
folders = os.listdir(path)
#check if one of the directory starts with the short_cut
for folder in folders:
    if folder.startswith(short_cut):
        print(path +'/'+ folder)
        if os.path.isdir(path +'/'+ folder):
            print(folder)
            #if so, set the folder to path + folder
            folder_rosbags = path +'/'+ folder
            print('playing rosbags in folder: ' + folder_rosbags)
            break
if folder == path:
    print('playing from default folder: ' + folder_rosbags)

# get all files in the folder
files = os.listdir(folder_rosbags)
# put a string together with "rosbag play " + all files
command = "rosbag play --skip-empty=1 "
for file in files:
    # if file starts with short_cut and ends with .bag
    if file.startswith(short_cut) and file.endswith(".bag"):
        # add the file to the command
        command += folder_rosbags + "/" + file + " "
# print the command
print(command)
# pause for 1 seconds
os.system("sleep 1")

# execute the command
os.system(command)