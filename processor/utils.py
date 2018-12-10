"""
Utility functions
"""
import os
import rasterio
import numpy as np
from pyproj import Proj
from pyproj import transform as proj_transform
from rasterio import transform as rio_transform


def transform_points(points):
    """
    Tranform the projection of points from WGS84 to Web Mercator
    Spatial analysis is usually under projected coordinate system.

    Parameters
    ----------
    points : [type]
        [description]
    
    """
    wgs_84 = Proj("+init=epsg:4326")
    web_mercator = Proj("+init=epsg:3857")

    trans_points = []
    for point in points:
        tp = proj_transform(wgs_84, web_mercator, point[0], point[1])
        trans_points.append(tp)

    return trans_points

def create_raster_dataset(data, x, y, raster_path):
    """[summary]
    
    Parameters
    ----------
    data : [type]
        [description]
    x : [type]
        [description]
    y : [type]
        [description]
    raster_path : [type]
        [description]
    
    Returns
    -------
    [type]
        [description]
    """
    try:
        height, width = data.shape
        
        west, east = x[0], x[-1]
        south, north = y[-1], y[0]
        affine = rio_transform.from_bounds(
            west=west,
            south=south,
            east=east,
            north=north,
            width=width,
            height=height
        )

        profile = {
            "count": 1,
            "driver": "GTiff",
            "crs": "epsg:3857",
            "transform": affine,
            "height": height,
            "width": width,
            "dtype": "float64",
            "nodata": np.nan,
            "tiled": False
        }
        
        with rasterio.open(raster_path, "w", **profile) as raster:
            raster.write(data, 1)

    except Exception as error:
        return False

    return True
