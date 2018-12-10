"""
Interpolation with given data
"""
from warnings import warn
import numpy as np
import scipy as sp
from scipy.interpolate import griddata
from processor.utils import transform_points


def simple_interpolate(points, values, resolution=100, method="linear"):
    """
    Use interpolation methods provided by Scipy
    """
    if method not in ["linear", "nearest", "cubic"]:
        method = "linear"
        warn("Set interpolate method to default 'linear'")
    
    trans_points = transform_points(points)

    x_vals = [point[0] for point in trans_points]
    y_vals = [point[1] for point in trans_points]
    x_min, x_max = min(x_vals), max(x_vals)
    y_min, y_max = min(y_vals), max(y_vals)
    
    x = np.arange(x_min, x_max, resolution)
    y = np.arange(y_min, y_max, resolution)
    grid_x, grid_y = np.meshgrid(x, y)

    data = griddata(trans_points, values, (grid_x, grid_y), method)

    return data, x, y


def kriging_interpolate():
    """
    Use Guassain Process Regression provided by Scikit-learn
    """
    pass
