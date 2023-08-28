#!/bin/bash
# $1: folder name where the folder $2 is inside (f.e. orb)
# $2: prefix and folder name of the bagfile (c7_orb_d435)

# check if $2 exists as folder
if [ ! -d "$1/$2" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  mkdir $1/$2
  echo "made directory $1/$2"
fi
# the name is a combination of $2 and _ and a consecutive number
# check if $2_$number.bag exists in a infinite while loop 
# if it does, continue, if it doesn't, break and use that name
# print the pwd
name=placeholder
number=0
while true; do
  name=$1/$2/$2_$number
  if [ -f "$name.bag" ]; then
    # Control will enter here if $name.bag exists.
    number=$((number+1))
  else
    # Control will enter here if $name.bag doesn't exist.
    break
  fi
done

rosbag record --buffsize 0 -O $name.bag \
/ground_truth/odom \
/orb_slam3/camera_pose \
/orb_slam3_ros/trajectory



# $1: prefix and folder name of the bagfile (c7_orb_d435)
# $2: folder name where the folder $2 is inside (f.e. orb/)