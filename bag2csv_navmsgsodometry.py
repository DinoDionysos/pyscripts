#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os

# get the name of the file that we are executing
file_name = os.path.basename(__file__)

# check if the user has provided the correct number of arguments
if len(sys.argv) != 4:
    print("Usage: python3 "+file_name+" <bag_name> <topic_name> <csv_name> \nThe files <bag_name> and <csv_name> should be placed in the bags and csv folders respectively. \nDo not add bag/ or csv/ in front of the file names.")
    sys.exit(1)

# read the first input from command line
first = sys.argv[1]
second = sys.argv[2]
third = sys.argv[3]

# create a string with "csv/" +  third + ".csv"
csv_file = "csv/" + third

command = 'rostopic echo -b bags/'+first+' -p '+second+' > '+csv_file
os.system(command)
# print the command
print("executing: " + command)

# load csv/test_orbmono_vs_gt-ground_truthodom.csv from /csv as dataframe
df = pd.read_csv(csv_file)
print("loaded: " + csv_file)
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

# save csv as cvs_file
df.to_csv(csv_file, index=False)
print("saved to: " + csv_file)