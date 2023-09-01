#!/bin/bash
# Call it from pyscripts/bags folder because of the relative paths
# $1: shortcut of the bag file (c11, c12, c13, ...)
# $2: folder name where the folder $2 will be inside (f.e. orb)
# $3: postfix of the roslaunch file (stereo, d435, mono)
# $4: number of runs / how many bagfiles to record (1, 25, ...)
# $5: folder where the bagfiles are stored and saved to ("/mnt/d/rosbags/")
# for example: bash n_record_slam.sh orb c11 d435 25

# $2 old: prefix and folder name of the bagfile to record (c7_orb_d435)
#make a variable for the folder name out of $2_$1_$3 (c7_orb_d435)
folder_and_prefix=$1_$2_$3

for i in $(seq 0 1 $4)
do
  echo "----------------------------------------------------------------"
  echo "Starting roslaunch"
  roslaunch orb_slam3_ros_wrapper taurob_$3.launch &
  pid_roslaunch=$!
  sleep 10
  echo "----------------------------------------------------------------"
  echo "Starting recording"
  sleep 0.5
  bash record_orb.sh $2 $folder_and_prefix $5 &
  sleep 1
  echo "----------------------------------------------------------------"
  echo "Starting playing"
  sleep 0.5
  # rosbag play c7_circle_lockstep_c4_frac.bag
  python3 play_cX.py $5 $1
  sleep 2
  killall record
  sleep 1
  kill $pid_roslaunch
  sleep 0.5
  echo "----------------------------------------------------------------"
  echo "Done with $i th run of $4: $1 $2 $3"
  echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
done

