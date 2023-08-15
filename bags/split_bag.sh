#!/bin/bash
# provide input bag, and time fraction
echo $1, $2, $3, $4
t0_rosbag=`rosbag info -y -k start $1`
t1_rosbag=`rosbag info -y -k end $1`
t0=`echo "$t0_rosbag + ($t1_rosbag - $t0_rosbag) * $3" | bc -l`
t1=`echo "$t0_rosbag + ($t1_rosbag - $t0_rosbag) * $4" | bc -l`
echo $t0_rosbag, $t1_rosbag, $t0, $t1
rosbag filter $1 $2_cut_$3_$4.bag "t.secs >= $t0 and t.secs <= $t1"


# two sided cut syntax
# rosbag filter input.bag output.bag "t.secs >= 1531425960 and t.secs <= 1531426140"