from rest_framework import serializers
from core.models.shared import Category, TruckType, Country
from core.models.project_info import ProjectInfo

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'uuid']


class TruckTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckType
        fields = ['name', 'uuid']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name_ar', 'uuid']


class ProjectInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectInfo
        fields = "__all__"
        read_only_fields = ("created", "modified")
