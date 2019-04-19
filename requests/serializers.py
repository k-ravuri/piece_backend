from rest_framework import serializers
from requests.models import Request

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        # fields = ('id', 'name', 'address', 'phonenumber')
        fields = '__all__'