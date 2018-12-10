import os
import json
import sys
import requests
from pprint import pprint
proj_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(proj_path)

from processor.geoserver import GeoserverService


def publish_wms_example():
    """[summary]
    
    """
    # Create wms for this raster file
    file_path = '/home/gu/Downloads/client_param_20181207220158.tif'

    # Set rest endpoint
    service_url = 'http://localhost:8080/geoserver/rest'
    service = GeoserverService(service_url=service_url)
    workspace_name = 'interpo'
    service_name = service.publish_wms(workspace_name, file_path)
    print(service_name)


if __name__ == '__main__':
    publish_wms_example()
