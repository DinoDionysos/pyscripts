import os
import sys
#1: short cut of rosbag
#2: (optional) folder path (default: current folder)

short_cut = sys.argv[1]
print(short_cut)
if len(sys.argv) > 2:
    folder = sys.argv[2]
else: 
    # get current folder path
    folder = os.path.dirname(os.path.realpath(__file__))
# get all files in the folder
files = os.listdir(folder)
# put a string together with "rosbag play " + all files
command = "rosbag play --skip-empty=1 "
for file in files:
    if file.endswith(".bag") and file.startswith(short_cut):
        command += folder + "/" + file + " "
# print the command
print(command)
# pause for 1 seconds
os.system("sleep 1")

# execute the command
os.system(command)
