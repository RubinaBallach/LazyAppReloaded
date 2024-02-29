from rest_framework import serializers
from .models import FlatApplication, FlatListing


# hope it is right so
class FlatApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlatApplication
        fields = '__all__'

class FlatListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlatListing
        fields = '__all__'
