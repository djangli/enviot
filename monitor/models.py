from django.db import models

# Create your models here.
class Site(models.Model):
    """[summary]
    
    Parameters
    ----------
    models : [type]
        [description]
    
    """
    name = models.TextField(max_length=30)
    lat = models.FloatField()
    lon = models.FloatField()

    class Meta:
        db_table = "site"
        verbose_name = "Site"
        verbose_name_plural = "Sites"


class Sensor(models.Model):
    """[summary]
    
    Parameters
    ----------
    models : [type]
        [description]
    
    """
    serial = models.TextField(max_length=30)
    site = models.ForeignKey(Site, related_name="sensors", on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "sensor"
        verbose_name = "Sensor"
        verbose_name_plural = "Sensors"


class Parameter(models.Model):
    """[summary]
    
    Parameters
    ----------
    models : [type]
        [description]
    
    """
    name = models.TextField(max_length=10)
    value = models.FloatField()
    units = models.TextField(max_length=20)
    created = models.DateTimeField()
    sensor = models.ForeignKey(Sensor, related_name="parameters", on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "parameter"
        verbose_name = "Parameter"
        verbose_name_plural = "Parameters"


class WebMapService(models.Model):
    """[summary]
    
    Parameters
    ----------
    models : [type]
        [description]
    
    """
    client = models.TextField(max_length=30)
    parameter = models.TextField(max_length=30)
    timestamp = models.TextField(max_length=30)
    endpoint = models.TextField(max_length=200)
    workspace = models.TextField(max_length=20)
    store_name = models.TextField(max_length=50)
    layer_name = models.TextField(max_length=30)
    file_path = models.TextField(max_length=30)
