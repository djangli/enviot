"""
Get sensor to work, and collect data.
"""
import os
import sys
from django.core.wsgi import get_wsgi_application

proj_path = '/home/ubuntu/enviot/'#os.path.dirname(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "enviot.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
application = get_wsgi_application()

from datetime import datetime
from random import randint
from monitor.models import Site, Parameter


def collect_data():
    """[summary]
    
    """
    number = 20
    if Parameter.objects.count() == 0:
        for i in range(number):
            site = Site.objects.get(name="Site_{}".format(i+1))
            sensor = site.sensors.all()[0]
            parameter = Parameter(
                name="CO2",
                value=randint(100, 500),
                units="ppm",
                created=datetime.now(),
                sensor=sensor
            )
            parameter.save()
        return
    
    points, values = [], []
    for parameter in Parameter.objects.all():
        parameter.value = randint(100, 500)
        parameter.created = datetime.now()
        parameter.save()

        site = parameter.sensor.site
        points.append((site.lon, site.lat))
        values.append(parameter.value)

    print("Parameter updated!")

if __name__ == "__main__":
    collect_data()
