from rest_framework import serializers
from locations.models import Governorate, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name_ar', 'governorate']


class GovernorateSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Governorate
        fields = ['id', 'governorate_name_ar', 'cities']
