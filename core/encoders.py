from rest_framework.utils.encoders import JSONEncoder
from django.contrib.gis.measure import Distance


class DistanceEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Distance):
            return obj.m
        return super(DistanceEncoder, self).default(obj)
