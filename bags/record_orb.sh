#!/bin/bash
# $1: folder name where the folder $2 wil be inside (f.e. orb)
# $2: prefix and folder name of the bagfile (c7_orb_d435)
# $3: folder where the bagfiles are stored and saved to ("/mnt/d/rosbags/")

folder=$3/$1/$2
# check if $2 exists as folder
if [ ! -d $folder ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  mkdir $folder
  echo "made directory $folder"
fi
# the name is a combination of $2 and _ and a consecutive number
# check if $2_$number.bag exists in a infinite while loop 
# if it does, continue, if it doesn't, break and use that name
# print the pwd
name=placeholder
number=0
while true; do
  name=$number
  # print $2_$number.bag
  echo $2_$number.bag
  echo $2
  if [ -f "$folder/$2_$name.bag" ]; then
    number=$((number+1))
  else
    break
  fi
done

rosbag record --buffsize 0 -O $folder/$2_$name.bag \
/ground_truth/odom \
/orb_slam3/camera_pose \
/orb_slam3_ros/trajectory



# $1: prefix and folder name of the bagfile (c7_orb_d435)
# $2: folder name where the folder $2 is inside (f.e. orb/)