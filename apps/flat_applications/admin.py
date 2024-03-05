from django.contrib import admin
from .models import LazyRenter, Landlord, LazyFlatApplication
# Register your models here.

@admin.register(LazyRenter)
class LazyRenterAdmin(admin.ModelAdmin):
    fields = [
        'renter_id', 'profile_id', 'first_name', 
        'last_name','date_of_birth', 
        'renter_mail','renter_phone',
        'current_address','current_occupation',
        'net_income','stable_income_available',
        'guarantee_available','clean_schufa_report',
        'references_available','long_term_leasing_desire',
        'quiet_and_tidy_tenant','pets','type_of_pets',
        'no_of_people','children','no_of_children']
    readonly_fields = ['renter_id', 'profile_id']

@admin.register(Landlord)
class LandlordAdmin(admin.ModelAdmin):
    fields = [
        'landlord_id', 'landlord_name',
        'landlord_contact', 'landlord_address',]
    readonly_fields = ['landlord_id']

@admin.register(LazyFlatApplication)
class LazyFlatApplicationAdmin(admin.ModelAdmin):
    fields = [
        'flat_application_id', 'renter_id', 'landlord_id',
        'flat_ad_link', 'title', 'city', 'postal_code',
        'district', 'kaltmiete', 'apartment_size',
        'deposit', 'rooms', 'extra_costs', 'heating_costs', 'total_cost',
        'additional_notes', 'flat_application_letter']
    readonly_fields = ['flat_application_id', 'renter_id', 'landlord_id', 'flat_ad_link']
