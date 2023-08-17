
import numpy as np
from util_hypothesis_tests_2 import read_cols_from_folder

def rmse(data: np.array):
    """rmse over the entries of array data"""
    return np.sqrt(np.mean(data**2))

def mae(data : np.array):
    """mae over the entries in array data"""
    return np.mean(np.abs(data))

def ate(data: np.array, ate_type = 'rmse'):
    """ate over the entries in array data"""
    if ate_type == 'rmse':
        return rmse(data)
    elif ate_type == 'mae':
        return mae(data)
    else:
        raise ValueError('invalid error type')
    
def ates_from_folder(folder, pose_error_type, trajectory_error_type = 'rmse'):
    """returns one ate per csv file in folder. ate are over a specific pose error"""
    columns = read_cols_from_folder(folder, pose_error_type)
    return ates_from_columns(columns, trajectory_error_type)

def ates_from_columns(columns, trajectory_error_type = 'rmse'):
    """returns one ate per column"""
    return np.array([ate(columns[i], trajectory_error_type) for i in range(0, len(columns))])
