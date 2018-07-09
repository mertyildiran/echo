from rest_framework.renderers import JSONRenderer
from core.encoders import DistanceEncoder

class DistanceRenderer(JSONRenderer):
    encoder_class = DistanceEncoder
