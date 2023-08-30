rosbag record --buffsize 0 --split --size 8196 -O /media/dino/Samsung_T5/rosbags/$1 \
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
/tf_static \