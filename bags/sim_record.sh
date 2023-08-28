rosbag record --buffsize 0 --split --size 8192 -O c8_fun \
/ground_truth/odom \
/realsense_d435/color/camera_info \
/realsense_d435/color/image_raw \
/realsense_d435/depth/camera_info \
/realsense_d435/depth/image_raw \
/stereo_camera/left/camera_info \
/stereo_camera/left/image_raw \
/stereo_camera/right/camera_info \
/stereo_camera/right/image_raw \
/taurob_tracker/imu/data \
# /tf \
/tf_static \