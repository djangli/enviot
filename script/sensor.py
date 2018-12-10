"""
For each site, install one sensor on it.
"""
import os
import sys
from django.core.wsgi import get_wsgi_application

proj_path = '/home/ubuntu/enviot/'#os.path.dirname(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "enviot.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
application = get_wsgi_application()

import string
from random import choice
from monitor.models import Site, Sensor


def install_sensors():
    """[summary]

    """
    number = 20
    if Sensor.objects.count() == number:
        return

    for i in range(number):
        site = Site.objects.get(name="Site_{}".format(i+1))
        serial = "".join(choice(string.ascii_letters) for _ in range(10))
        
        sensor = Sensor(serial=serial, site=site)
        sensor.save()


if __name__ == "__main__":
    install_sensors()
