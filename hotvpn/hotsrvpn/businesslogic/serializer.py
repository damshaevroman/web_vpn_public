from rest_framework import serializers
from hotsrvpn.models import Hotel, Hotel_User



class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        exclude = ('hotel_ping_status',)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel_User
        fields = '__all__'
