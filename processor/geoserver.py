"""
Wrap geoserver rest api
"""
import json
import os
import requests
import warnings
from pprint import pprint


class GeoserverService(object):
    """[summary]
    
    Parameters
    ----------
    object : [type]
        [description]
    
    """

    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    def __init__(self, service_url, admin='admin', password='geoserver'):
        self.service_url = service_url.rstrip('/')
        self.auth=(admin, password)
    
    def list_workspaces(self):
        """[summary]
        
        """
        url = f'{self.service_url}/workspaces.json'
        
        response = requests.get(url, auth=self.auth, headers=self.headers)
        if response.status_code != '200':
            response.raise_for_status()
        
        workspaces = response.json()['workspaces']['workspace']
        return workspaces
    
    def get_workspace(self, workspace_name):
        """[summary]
        
        Parameters
        ----------
        workspace_name : [type]
            [description]
        
        """
        url = f'{self.service_url}/workspaces/{workspace_name}.json'
        
        response = requests.get(url, auth=self.auth, headers=self.headers)
        if response.status_code != '200':
            response.raise_for_status()
        
        workspace = response.json()['workspace']
        return workspace
    
    def list_coverage_stores(self, workspace_name):
        """[summary]
        
        Parameters
        ----------
        workspace_name : [type]
            [description]
        
        Returns
        -------
        [type]
            [description]
        """
        url = f'{self.service_url}/workspaces/{workspace_name}/coveragestores.json'
    
        response = requests.get(url, auth=self.auth, headers=self.headers)

        if response.status_code != '200':
            return []
        
        coverage_stores = response.json()['coverageStores']['coverageStore']
        return coverage_stores

    def get_coverage_store(self, workspace_name, store_name):
        """[summary]
        
        Parameters
        ----------
        workspace_name : [type]
            [description]
        store_name : [type]
            [description]
        
        """
        url = f'{self.service_url}/workspaces/{workspace_name}/coveragestores/{store_name}.json'

        response = requests.get(url, auth=self.auth, headers=self.headers)
        if response.status_code != '200':
            response.raise_for_status()
        
        coverage_store = response.json()['coverageStore']
        return coverage_store
    
    def create_coverage_store(self, workspace_name, file_path, store_name=None, format='GeoTIFF', enabled=True):
        """[summary]
        
        Parameters
        ----------
        workspace : [type]
            [description]
        file_path : [type]
            [description]
        format : str, optional
            [description] (the default is 'GeoTIFF', which [default_description])
        
        """
        if not store_name:
            store_name = os.path.basename(os.path.splitext(file_path)[0])
        
        # Check coverage stores
        coverage_stores = self.list_coverage_stores(workspace_name)
        for coverage_store in coverage_stores:
            if coverage_store['name'] != store_name:
                continue
            warnings.warn(f'Coverage store {store_name} under {workspace_name} already exists!!!')
            return self.get_coverage_store(workspace_name, store_name)

        payload = {
            'coverageStore': {
                'name': store_name,
                'workspace': workspace_name,
                'type': format,
                'url': 'file://' + file_path,
                'enabled': enabled
            }
        }

        url = f'{self.service_url}/workspaces/{workspace_name}/coveragestores.json'
        response = requests.post(url, data=json.dumps(payload), auth=self.auth, headers=self.headers)
        if response.status_code != '201':
            print('Error: ', response.status_code)
            response.raise_for_status()

        coverage_store = self.get_coverage_store(workspace_name, store_name)
        return coverage_store

    def list_coverage_layers(self, workspace_name, store_name):
        """[summary]
        
        Parameters
        ----------
        workspace_name : [type]
            [description]
        store_name : [type]
            [description]
        
        Returns
        -------
        [type]
            [description]
        """
        url = f'{self.service_url}/workspaces/{workspace_name}/coveragestores/{store_name}/coverages.json'
        
        response = requests.get(url, auth=self.auth, headers=self.headers)
        if response.status_code != '200':
            return []
        
        coverages = response.json()['coverages']
        if not coverages:
            return []

        return coverages['coverage']

    def get_coverage_layer(self, workspace_name, store_name, coverage_name):
        """[summary]
        
        Parameters
        ----------
        workspace_name : [type]
            [description]
        store_name : [type]
            [description]
        coverage_name : [type]
            [description]
        
        Returns
        -------
        [type]
            [description]
        """
        url = f'{self.service_url}/workspaces/{workspace_name}/coveragestores/{store_name}/coverages/{coverage_name}.json'
        
        response = requests.get(url, auth=self.auth, headers=self.headers)
        
        if response.status_code == '404':
            return {}

        if response.status_code != '200':
            response.raise_for_status()
        
        coverage = response.json()['coverage']
        return coverage

    def create_coverage_layer(self, workspace_name, store_name, coverage_name):
        """[summary]
        
        Parameters
        ----------
        workspace_name : [type]
            [description]
        store_name : [type]
            [description]
        
        """
        # Check coverage layers
        coverage_layers = self.list_coverage_layers(workspace_name, store_name)
        for coverage_layer in coverage_layers:
            if coverage_layer['name'] != coverage_name:
                continue
            warnings.warn(f'Coverage layer {coverage_name} under {workspace_name} already exists!!!')
            return self.get_coverage_layer(workspace_name, store_name, coverage_name)
        
        if not store_name:
            store_name = coverage_name
        
        url = f'{self.service_url}/workspaces/{workspace_name}/coveragestores/{store_name}/coverages.json'
        payload = {
            'coverage': {
                'name': coverage_name,
                'nativeName': coverage_name
            }
        }
        response = requests.post(url, data=json.dumps(payload), auth=self.auth, headers=self.headers)
        if response.status_code != '201':
            response.raise_for_status()
        
        return self.get_coverage_layer(workspace_name, store_name, coverage_name)
        
    def publish_wms(self, workspace_name, file_path):
        """[summary]
        
        Parameters
        ----------
        workspace_name : [type]
            [description]
        file_path : [type]
            [description]
        
        """
        coverage_store = self.create_coverage_store(workspace_name, file_path)
        store_name = coverage_store['name']
        coverage_layer = self.create_coverage_layer(workspace_name, store_name, coverage_name=store_name)
        coverage_name = coverage_layer['title']
        return f'{workspace_name}:{coverage_name}'


if __name__ == "__main__":
    service = GeoserverService(service_url='http://ec2-18-234-73-227.compute-1.amazonaws.com:8080/geoserver/rest')
    
    # Get a coverage store
    file_path = '/home/gu/Downloads/client_param_20181207220158.tif'
    store_name = 'client_param_20181207220158'
    # result = service.create_coverage_store(workspace_name='interpo', file_path=file_path)
    # pprint(result)

    # Create a coverage layer
    # store_name = 'client_parameter_20181206220956'
    # result = service.get_coverage_layer(workspace_name='interpo', store_name=store_name, coverage_name=store_name)
    # result = service.create_coverage_layer(workspace_name='interpo', store_name=store_name, coverage_name=store_name)
    # pprint(result)

    # result = service.create_coverage_layer(workspace_name='interpo', store_name=store_name, coverage_name=store_name)
    # pprint(result)
    result = service.publish_wms(workspace_name='interpo', file_path=file_path)
    pprint(result)
