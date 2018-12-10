"""
Monitor views
"""
import os
from datetime import datetime

import requests
from django.http import HttpResponse, Http404, FileResponse
import rasterio

from rest_framework.generics import ListCreateAPIView
from enviot.settings import MEDIA_ROOT
from monitor.models import Site, Sensor, Parameter, WebMapService
from monitor.serializers import SiteSerializer, SensorSerializer, ParameterSerializer
from script.parameter import collect_data
from processor.geoserver import GeoserverService
from processor.interpolate import simple_interpolate
from processor.utils import create_raster_dataset


class SiteListCreateAPIView(ListCreateAPIView):
    """[summary]
    
    Parameters
    ----------
    ListCreateAPIView : [type]
        [description]
    
    """
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """
        collect_data()

        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response


class SensorListCreateAPIView(ListCreateAPIView):
    """[summary]
    
    Parameters
    ----------
    ListCreateAPIView : [type]
        [description]
    
    """
    queryset = Site.objects.all()
    serializer_class = SensorSerializer


class ParameterListCreateAPIView(ListCreateAPIView):
    """[summary]
    
    Parameters
    ----------
    ListCreateAPIView : [type]
        [description]
    
    """
    queryset = Site.objects.all()
    serializer_class = ParameterSerializer


def interpolate_map(request):
    """[summary]
    
    Parameters
    ----------
    request : [type]
        [description]
    
    Returns
    -------
    [type]
        [description]
    """

    sites = Site.objects.all()

    # extract points/values
    points = [(site.lon, site.lat) for site in sites]
    values = [site.sensors.all()[0].parameters.all()[0].value for site in sites]
    data, x, y = simple_interpolate(points, values)

    # prepare
    client_name = 'Colorado'
    parameter_name = 'CO2'
    timestamp = str(datetime.now().timestamp()).replace('.', '_')
    layer_name = f'{client_name}_{parameter_name}_{timestamp}'
    file_name = layer_name + '.tif'

    # interpolate
    raster_path = os.path.join(MEDIA_ROOT, file_name)
    if os.path.exists(raster_path):
        os.remove(raster_path)
    result = create_raster_dataset(data, x, y, raster_path)
    
    # index result
    service = WebMapService(
        client=client_name,
        parameter=parameter_name,
        timestamp=timestamp,
        workspace='interpo',
        store_name=layer_name,
        layer_name=layer_name,
        file_path=raster_path
    )
    service.save()

    return HttpResponse(content=b"<a id='result-link' href='/download-map/' download>interpolation map</a>")


def publish_web_map_service(request):
    """[summary]
    
    Parameters
    ----------
    request : [type]
        [description]
    
    """
    # publish geoserver wms layer
    workspace = 'interpo'
    service_url = 'http://ec2-18-234-73-227.compute-1.amazonaws.com:8080/geoserver/rest'
    
    service = WebMapService.objects.last()
    service.endpoint = service_url
    service.workspace = workspace

    geoserver_service = GeoserverService(service_url=service_url)
    service_layer = geoserver_service.publish_wms(workspace_name=workspace, file_path=service.file_path)

    return HttpResponse(content=bytes(service_layer, 'utf-8'))


def download_map(request):
    """[summary]
    
    Parameters
    ----------
    request : [type]
        [description]
    
    """
    service = WebMapService.objects.last()
    raster_path = service.file_path
    file_name = os.path.basename(raster_path)

    with open(raster_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type='application/tif')
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        return response


def show_map(request):
    """[summary]
    
    Parameters
    ----------
    request : [type]
        [description]
    
    """
    # publish geoserver wms layer
    service = WebMapService.objects.last()
    service_layer = f'{service.workspace}:{service.layer_name}'
    return HttpResponse(content=bytes(service_layer, 'utf-8'))
