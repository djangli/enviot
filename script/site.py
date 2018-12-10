"""
Setup 20 monitoring site around Fort Collins area.
"""
import os
import sys
from django.core.wsgi import get_wsgi_application

proj_path = '/home/ubuntu/enviot/'#os.path.dirname(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "enviot.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
application = get_wsgi_application()

from random import uniform
from monitor.models import Site


def setup_sites():
    """[summary]
    
    """
    number = 20

    if Site.objects.count() == number:
        return

    # Area around Fort Collins
    minx, miny, maxx, maxy = (-106.084419, 39.585258, -104.084419, 41.585258)

    # Generate 20 sites
    for i in range(number):
        lat = uniform(miny, maxy)
        lon = uniform(minx, maxx)
        name = "Site_{}".format(i+1)
        site = Site(name=name, lat=lat, lon=lon)
        site.save()


if __name__ == "__main__":
    setup_sites()
