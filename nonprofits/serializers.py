from rest_framework import serializers
from nonprofits.models import Nonprofit

class NonprofitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nonprofit
        fields = '__all__'