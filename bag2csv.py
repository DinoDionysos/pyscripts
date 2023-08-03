#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os

# get the name of the file that we are executing
file_name = os.path.basename(__file__)
print(len(sys.argv))
# check if the user has provided the correct number of arguments
if len(sys.argv) > 4 or len(sys.argv) < 3:
    print("[INFO] "+file_name+" | Usage: python3 "+file_name+" <bag_name> <topic_name> optional:<topic_type> \nThe file <bag_name> should be placed in the bags folder respectively. \nIt is not necessary to have 'bags/' in the beginning of the <bag_name>.\n <topic_type> is optional and can be found by executing: 'rosbag info <bag_name> -y -k topics'\n <topic_name> has a '/' in the beginning.")
    sys.exit(1)

# read the first input from command line
bag_name = sys.argv[1]
# if bag_name starts with bags/, remove it
if bag_name.startswith('bags/'):
    bag_name = bag_name.replace('bags/', '')
topic_name = sys.argv[2]

if len(sys.argv) == 4:
    topic_type = sys.argv[3]
else:
    # excecute the command: "rosbag info test_orbmono_vs_gt.bag -y -k topics" and read the output into a variable
    output = os.popen('rosbag info bags/'+bag_name+' -y -k topics').read()
    print(output)

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
            print("[INFO] "+file_name+" | found topic name in bag info: " + topic_name)
            # get the word between "type:" and "\n"
            topic_type = cell.split('type: ')[1].split('\n')[0]
            print("[INFO] "+file_name+" | found topic type: " + topic_type)

    if topic_type == "":
        print("[INFO] "+file_name+" | The topic type could not be resolved from the topic name: " + topic_name + " and the bag: " + bag_name + ".\nPlease provide the topic type as the third argument. f.e. nav_msgs/Odometry")
        sys.exit(1)


# make csv_file the combination of first and second
csv_file = bag_name + '-' + topic_name
# replace the / with -
csv_file = csv_file.replace('/', '-')
# replace the . with -
csv_file = csv_file.replace('.', '-')
# add .csv to the end of csv_file and place it in the csv folder
csv_file = "csv/" + csv_file + '.csv'

command = 'rostopic echo -b bags/'+bag_name+' -p '+topic_name+' > '+csv_file
os.system(command)
# print the command
print("[INFO] "+file_name+" | executing: " + command)

# load csv/test_orbmono_vs_gt-ground_truthodom.csv from /csv as dataframe
df = pd.read_csv(csv_file)
print("[INFO] "+file_name+" | loaded: " + csv_file)



# define function to replace the following part
if (topic_type == "nav_msgs/Odometry"):
    # drop the all columns with twist in the name
    df = df[df.columns.drop(list(df.filter(regex='twist')))]
    # drop all the columns with covariance in the name
    df = df[df.columns.drop(list(df.filter(regex='covariance')))]
    # drop all the columns with orientation in the name
    df = df[df.columns.drop(list(df.filter(regex='orientation')))]
    # remove the "field." from the column names
    df.columns = df.columns.str.replace('field.', '')
    # remove the "pose." from the column names
    df.columns = df.columns.str.replace('pose.', '')
    # remove the "position." from the column names
    df.columns = df.columns.str.replace('position.', '')
    # remove the "header." from the column names
    df.columns = df.columns.str.replace('header.', '')

elif (topic_type == "geometry_msgs/PoseStamped"):
    # drop the all columns with twist in the name
    df = df[df.columns.drop(list(df.filter(regex='twist')))]
    # drop all the columns with covariance in the name
    df = df[df.columns.drop(list(df.filter(regex='covariance')))]
    # drop all the columns with orientation in the name
    df = df[df.columns.drop(list(df.filter(regex='orientation')))]
    # remove the "field." from the column names
    df.columns = df.columns.str.replace('field.', '')
    # remove the "pose." from the column names
    df.columns = df.columns.str.replace('pose.', '')
    # remove the "position." from the column names
    df.columns = df.columns.str.replace('position.', '')
    # remove the "header." from the column names
    df.columns = df.columns.str.replace('header.', '')

# normalize the timestamp column
df['stamp'] = df['stamp'] - df['stamp'][0]
# normalize the seq column
df['seq'] = df['seq'] - df['seq'][0]
# normalize the %time column
df['%time'] = df['%time'] - df['%time'][0]
# normalize the x column
df['x'] = df['x'] - df['x'][0]
# normalize the y column
df['y'] = df['y'] - df['y'][0]
# normalize the z column
df['z'] = df['z'] - df['z'][0]

# save csv as csv_file
df.to_csv(csv_file, index=False)
print("[INFO] "+file_name+" | saved to: " + csv_file)