from rest_framework import serializers
from .models import LazyFlatApplication, LazyRenter, Landlord


class LandlordSerializer(serializers.ModelSerializer):
    landlord_id = serializers.IntegerField(read_only=True)
    landlord_contact = serializers.CharField(max_length=200, required=False)
    class Meta:
        model = Landlord
        fields = '__all__'

class LazyRenterSerializer(serializers.ModelSerializer):
    renter_id = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = LazyRenter
        fields = '__all__'


class LazyFlatApplicationSerializer(serializers.Serializer):
    flat_application_id = serializers.IntegerField(read_only=True)
    renter_id = serializers.PrimaryKeyRelatedField(read_only=True)
    landlord_id = serializers.PrimaryKeyRelatedField(read_only=True)

    # information to be scraped from flat add and stored in Landlords
    flat_ad_link = serializers.URLField(max_length=300, required=False)
    title = serializers.CharField(max_length=100, required=False)
    city = serializers.CharField(max_length=50, required=False)
    postal_code = serializers.CharField(max_length=20, required=False)
    district = serializers.CharField(max_length=50, required=False)
    kaltmiete = serializers.CharField(max_length=20, required=False)
    apartment_size = serializers.CharField(max_length=20, required=False)
    deposit = serializers.CharField(max_length=20, required=False)
    rooms = serializers.CharField(max_length=20, required=False)
    extra_costs = serializers.CharField(max_length=20, required=False)
    heating_costs = serializers.CharField(max_length=100, required=False)
    total_cost = serializers.CharField(max_length=20, required=False)

    additional_notes = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)
    flat_application_letter = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)
    flat_application_costs = serializers.FloatField(read_only=True)

    landlord = LandlordSerializer(source="landlord_id", read_only=True)
    renter = LazyRenterSerializer(source="renter_id", read_only=True)

    class Meta:
        model = LazyFlatApplication
        fields = (
            "flat_application_id",
            "renter_id",
            "landlord_id",
            "flat_ad_link",
            "title",
            "city",
            "postal_code",
            "district",
            "kaltmiete",
            "apartment_size",
            "deposit",
            "rooms",
            "extra_costs",
            "heating_costs",
            "total_cost",
            "additional_notes",
            "flat_application_letter",
            "flat_application_costs",
            "landlord",
            "renter",
        )

    def update(self, instance, validated_data):
        instance.flat_ad_link = validated_data.get("flat_ad_link", instance.flat_ad_link)
        instance.title = validated_data.get("title", instance.title)
        instance.city = validated_data.get("city", instance.city)
        instance.postal_code = validated_data.get("postal_code", instance.postal_code)
        instance.district = validated_data.get("district", instance.district)
        instance.kaltmiete = validated_data.get("kaltmiete", instance.kaltmiete)
        instance.apartment_size = validated_data.get("apartment_size", instance.apartment_size)
        instance.deposit = validated_data.get("deposit", instance.deposit)
        instance.rooms = validated_data.get("rooms", instance.rooms)
        instance.extra_costs = validated_data.get("extra_costs", instance.extra_costs)
        instance.heating_costs = validated_data.get("heating_costs", instance.heating_costs)
        instance.total_cost = validated_data.get("total_cost", instance.total_cost)
        instance.additional_notes = validated_data.get("additional_notes", instance.additional_notes)
        instance.flat_application_letter = validated_data.get("flat_application_letter", instance.flat_application_letter)
        instance.flat_application_costs = validated_data.get("flat_application_costs", instance.flat_application_costs)
        instance.save()
        return instance


class LazyFlatApplicationDashboardSerializer(serializers.Serializer):
    """Serializer class used to display and update flat applications in the dashboard"""
    flat_application_id = serializers.IntegerField(read_only=True)
    renter_id = serializers.PrimaryKeyRelatedField(read_only=True)
    landlord_id = serializers.PrimaryKeyRelatedField(read_only=True)
    # information to be scraped from flat add and stored in Landlords
    flat_ad_link = serializers.URLField(max_length=300, required=False)
    title = serializers.CharField(max_length=100, required=False)
    city = serializers.CharField(max_length=50, required=False)
    postal_code = serializers.CharField(max_length=20, required=False)
    district = serializers.CharField(max_length=50, required=False)
    kaltmiete = serializers.CharField(max_length=20, required=False)
    apartment_size = serializers.CharField(max_length=20, required=False)
    deposit = serializers.CharField(max_length=20, required=False)
    rooms = serializers.CharField(max_length=20, required=False)
    extra_costs = serializers.CharField(max_length=20, required=False)
    heating_costs = serializers.CharField(max_length=100, required=False)
    total_cost = serializers.CharField(max_length=20, required=False)
    additional_notes = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)
    flat_application_costs = serializers.FloatField(read_only=True)

    class Meta:
        model = LazyFlatApplication
        fields = ("__all__")


    def update(self, instance, validated_data):
        instance.flat_ad_link = validated_data.get("flat_ad_link", instance.flat_ad_link)
        instance.title = validated_data.get("title", instance.title)
        instance.city = validated_data.get("city", instance.city)
        instance.postal_code = validated_data.get("postal_code", instance.postal_code)
        instance.district = validated_data.get("district", instance.district)
        instance.kaltmiete = validated_data.get("kaltmiete", instance.kaltmiete)
        instance.apartment_size = validated_data.get("apartment_size", instance.apartment_size)
        instance.deposit = validated_data.get("deposit", instance.deposit)
        instance.rooms = validated_data.get("rooms", instance.rooms)
        instance.extra_costs = validated_data.get("extra_costs", instance.extra_costs)
        instance.heating_costs = validated_data.get("heating_costs", instance.heating_costs)
        instance.total_cost = validated_data.get("total_cost", instance.total_cost)
        instance.additional_notes = validated_data.get("additional_notes", instance.additional_notes)
        instance.flat_application_costs = validated_data.get("flat_application_costs", instance.flat_application_costs)
        instance.save()
        return instance