from django.urls import path
from monitor import views

urlpatterns = [
    path("api/site-list/", views.SiteListCreateAPIView.as_view(), name="site-list"),
    path("api/sensor-list/", views.SensorListCreateAPIView.as_view(), name="sensor-list"),
    path("api/parameter-list/", views.ParameterListCreateAPIView.as_view(), name="parameter-list"),
    path("interpolate-map/", views.interpolate_map, name="interpolate-map"),
    path("download-map/", views.download_map, name="download-map"),
    path("publish-wms/", views.publish_web_map_service, name="publish-wms"),
    path("show-map/", views.show_map, name="show-map")
]
