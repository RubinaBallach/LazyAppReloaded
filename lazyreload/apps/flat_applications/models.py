from django.db import models

# Create your models here.
class Landlord(models.Model):
    landlord_id = models.AutoField(primary_key=True)
    landlord_name = models.CharField(max_length=60, blank=False)
    landlord_mail = models.EmailField(max_length=60, blank=True)
    landlord_phone = models.CharField(max_length=60, blank=True)
    landlord_address = models.TextField(blank=False)
    LANDLORD_TYPE_CHOICES = [
        ("private", "Private"),
        ("company", "Company"),
        ("agent", "Agent"),
    ]
    landlord_type = models.CharField(max_length=50, choices=LANDLORD_TYPE_CHOICES, default="private", blank=False)
    landlord_notes = models.TextField(blank=True)

# class LazyRenter(models.Model):
#     renter_id = models.AutoField(primary_key=True)
#     lazy_profile_id = models.ForeignKey(
#         "users.LazyUserProfile",
#         on_delete=models.CASCADE)
#     renter_mail = models.EmailField(max_length=60, blank=True)
#     renter_phone = models.CharField(max_length=60, blank=True)
#     renter_address = models.TextField(blank=True)
#     no_of_people = models.IntegerField(blank=True,
#                                        null=True,
#                                        verbose_name="Number of People to move"
#                                        )
#     children = models.IntegerField(default=False,
#                                    verbose_name="No. of children")
#     net_income = models.IntegerField(blank=True,
#                                      null=True,
#                                      verbose_name="Net Income per month"
#                                      )
#     move_in_date = models.DateField(blank=True, null=True)
#     pets = models.BooleanField(default=False, verbose_name="Pets")
#     type_of_pets = models.CharField(max_length=60, blank=True)
#     mention_pets = models.BooleanField(default=False, verbose_name="Mention Pets")


# class LazyFlatApplication(models.Model):
#     flat_application_id = models.AutoField(primary_key=True)
#     renter_id = models.ForeignKey(
#         LazyRenter,
#         on_delete=models.CASCADE)
#     flat_ad_link = models.URLField(max_length=300, blank=False)

#     # information to be scraped from flat add and stored in Landlords
#     landlord_id = models.ForeignKey(
#         Landlord,
#         on_delete=models.CASCADE,
#         blank=False)



class ApplicationLetter(models.Model):
    # Personal Information
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    current_address = models.TextField()
    marital_status = models.CharField(max_length=50) #maybe set single as default? not sure

    # Professional Information
    current_occupation = models.CharField(max_length=255)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)

    # Financial Stability
    stable_income_available = models.BooleanField(default=True)
    guarantee_available = models.BooleanField(default=False)
    clean_schufa_report = models.BooleanField(default=True)

    # References
    references_available = models.BooleanField(default=False)

    # Intent to Lease
    long_term_leasing_desire = models.BooleanField(default=True)

    # Responsibility
    quiet_and_tidy_tenant = models.BooleanField(default=True)
    

    # Pets
    pets = models.BooleanField(default=False)

    # Contact Information
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField()

    

    # Quantity of Children and People Moving In
    quantity_of_children = models.PositiveIntegerField(default=0)
    quantity_of_people_moving_in = models.PositiveIntegerField(default=1)

    # Additional Notes
    additional_notes = models.TextField(blank=True, null=True)