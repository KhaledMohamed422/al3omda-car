from rest_framework import serializers
from locations.models import Governorate, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name_ar', 'city_name_en', 'governorate']


class GovernorateSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Governorate
        fields = ['id', 'governorate_name_ar', 'governorate_name_en', 'cities']
