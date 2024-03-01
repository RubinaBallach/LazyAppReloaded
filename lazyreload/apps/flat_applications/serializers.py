from rest_framework import serializers
from .models import LazyFlatApplication, LazyRenter, Landlord


class LandlordSerializer(serializers.ModelSerializer):
    landlord_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Landlord
        fields = '__all__'

class LazyRenterSerializer(serializers.ModelSerializer):
    profile_id = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = LazyRenter
        fields = '__all__'


class LazyFlatApplicationSerializer(serializers.Serializer):
    class Meta:
        model = LazyFlatApplication
        fields = '__all__'
