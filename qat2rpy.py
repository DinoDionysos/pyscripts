
import numpy as np

#source: github copilot
#works
def qat2rpy(x,y,z,w):
    # roll (x-axis rotation)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = np.arctan2(sinr_cosp, cosr_cosp)

    # pitch (y-axis rotation)
    sinp = 2 * (w * y - z * x)
    if np.abs(sinp) >= 1:
        pitch = np.copysign(np.pi / 2, sinp)  # use 90 degrees if out of range
    else:
        pitch = np.arcsin(sinp)

    # yaw (z-axis rotation)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = np.arctan2(siny_cosp, cosy_cosp)
    return roll, pitch, yaw, 
 

# source:https://stackoverflow.com/questions/5782658/extracting-yaw-from-a-quaternion
def qat2rpy2(x,y,z,w):
    roll  = np.arctan2(2.0 * (w * y + z * x) , 1.0 - 2.0 * (x * x + y * y))
    pitch = np.arcsin(2.0 * (y * w - z * x))
    yaw   = np.arctan2(2.0 * (z * w + x * y) , - 1.0 + 2.0 * (w * w + x * x))
    return roll, pitch, yaw

#source:https://robotics.stackexchange.com/questions/16471/get-yaw-from-quaternion
def qat2yaw(x,y,z,w):
    yaw =np.arctan2(2 * (w * z + x * y), w * w + x * x - y * y - z * z)
    return yaw

 # source:https://stackoverflow.com/questions/5782658/extracting-yaw-from-a-quaternion
 #only for normalized qaterninons?
# def qat2rpy1(x,y,z,w):
#     yaw = np.arctan2(2.0*(y*z + w*x), w*w - x*x - y*y + z*z)
#     pitch = np.arcsin(-2.0*(x*z - w*y))
#     roll = np.arctan2(2.0*(x*y + w*z), w*w + x*x - y*y - z*z)
#     return roll, pitch, yaw
