from rest_framework import serializers
from .models import Installed_packeges, Task_and_Status
from hotsrvpn.models import Hotel


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class DeployDataSerializer(serializers.Serializer):
    client_login = serializers.CharField(max_length=100)
    client_ip = serializers.IPAddressField()
    client_port = serializers.CharField(max_length=100)
    client_password = serializers.CharField(max_length=100)
    client_sudo_password = serializers.CharField(max_length=100)


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task_and_Status
        fields = '__all__'


class InstalledPackegesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installed_packeges
        fields = '__all__'
