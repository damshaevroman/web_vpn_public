from rest_framework import routers, serializers, viewsets
from .models import ConfigServer

class ConfigSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConfigServer
        fields = '__all__'
