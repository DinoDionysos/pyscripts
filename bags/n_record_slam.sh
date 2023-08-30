#!/bin/bash
# Call it from pyscripts/bags folder because of the relative paths
# $1: folder name where the folder $2 is inside (f.e. orb)
# $2: prefix and folder name of the bagfile to record (c7_orb_d435)
# $3: postfix of the roslaunch file
# $4: number of runs / how many bagfiles to record 

for i in $(seq 1 1 $4)
do
  echo "----------------------------------------------------------------"
  echo "Starting roslaunch"
  roslaunch orb_slam3_ros_wrapper taurob_$3.launch &
  pid_roslaunch=$!
  sleep 10
  echo "----------------------------------------------------------------"
  echo "Starting recording"
  sleep 0.5
  bash record_orb.sh $1 $2 &
  sleep 1
  echo "----------------------------------------------------------------"
  echo "Starting playing"
  sleep 0.5
  # rosbag play c7_circle_lockstep_c4_frac.bag
  python3 play_cX.py c8
  sleep 2
  killall record
  sleep 1
  kill $pid_roslaunch
  sleep 0.5
  echo "----------------------------------------------------------------"
  echo "Done with $i th run of $4: $1 $2 $3"
  echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
done



# $1: postfix of the roslaunch file
# $2: prefix and folder name of the bagfile (c7_orb_d435)
# $3: folder name where the folder $2 is inside (f.e. orb/)
# $4: number of runs / how many bagfiles to record 