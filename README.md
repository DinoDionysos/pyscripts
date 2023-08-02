# Python scripts
The repository contains Python scripts that help handle trajectories, gathered as ROS bags. The rosbags are expected to be in a directory called "bags". The csv files get saved to csv/ directory. The following functionalities are covered:

- `bag2csv.py` - convert all the messages of a topic from a rosbag into a csv file.
    - supported messages: nav_msgs/Odometry, geometry_msgs/PoseStamped.
- `plot_timestamps_and_trajectory.py` - plots the trajectories and the timestamps of the messages in two seperate plots.
- `interpolate.py` - equalises the length of a ground_truth data series and a sampled data series
- `rotate_coor.py` - uses the Kapsch algorithm to align the trajectories.

All scripts take pathes to the respective files (.csv, .bag, ...) as inputs. See `compare.sh` for an example.