from rest_framework import serializers

from monitor.models import Site, Sensor, Parameter


class ParameterSerializer(serializers.ModelSerializer):
    """[summary]
    
    Parameters
    ----------
    serializers : [type]
        [description]
    
    """
    class Meta:
        model = Parameter
        fields = "__all__"


class SensorSerializer(serializers.ModelSerializer):
    """[summary]
    
    Parameters
    ----------
    serializers : [type]
        [description]
    
    """
    parameters = ParameterSerializer(many=True, read_only=True)
    class Meta:
        model = Sensor
        fields = "__all__"


class SiteSerializer(serializers.ModelSerializer):
    """[summary]
    
    Parameters
    ----------
    serializers : [type]
        [description]
    
    """
    sensors = SensorSerializer(many=True, read_only=True)

    class Meta:
        model = Site
        fields = "__all__"

