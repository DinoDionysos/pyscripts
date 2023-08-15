import os
import sys

folder = sys.argv[1]
# get all files in the folder
files = os.listdir(folder)
# put a string together with "rosbag play " + all files
command = "rosbag play "
for file in files:
    command += folder + "/" + file + " "
# print the command
print(command)
# pause for 5 seconds
os.system("sleep 10")

# execute the command
os.system(command)