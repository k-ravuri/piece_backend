from rest_framework import serializers
from dishes.models import Dish

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        # fields = ('id', 'name', 'address', 'phonenumber')
        fields = '__all__'