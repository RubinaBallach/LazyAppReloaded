from django.db import models

# Create your models here.
class Landlord(models.Model):
    landlord_id = models.AutoField(primary_key=True)
    landlord_name = models.CharField(max_length=60, blank=False)
    landlord_mail = models.EmailField(max_length=60, blank=True)
    landlord_phone = models.CharField(max_length=60, blank=True)
    landlord_address = models.TextField(blank=False)
    LANDLORD_TYPE_CHOICES = {
        "private": "Private",
        "company": "Company",
        "agent": "Agent",
    }
    landlord_type = models.CharField(choices=LANDLORD_TYPE_CHOICES, default="private", max_length=20, blank=False)
    landlord_notes = models.TextField(blank=True)

class LazyRenter(models.Model):
    renter_id = models.AutoField(primary_key=True)
    profile_id = models.ForeignKey(
        "users.LazyUserProfile",
        on_delete=models.CASCADE)
    renter_mail = models.EmailField(max_length=60, blank=True)
    renter_phone = models.CharField(max_length=60, blank=True)
    renter_address = models.TextField(blank=True)
    no_of_people = models.IntegerField(blank=True,
                                       null=True,
                                       verbose_name="Number of People to move"
                                       )
    children = models.IntegerField(default=False,
                                   verbose_name="No. of children")
    net_income = models.IntegerField(blank=True,
                                     null=True,
                                     verbose_name="Net Income per month"
                                     )
    move_in_date = models.DateField(blank=True, null=True)
    pets = models.BooleanField(default=False, verbose_name="Pets")
    type_of_pets = models.CharField(max_length=60, blank=True)
    mention_pets = models.BooleanField(default=False, verbose_name="Mention Pets")


class LazyFlatApplication(models.Model):
    flat_application_id = models.AutoField(primary_key=True)
    renter_id = models.ForeignKey(
        LazyRenter,
        on_delete=models.CASCADE)
    flat_ad_link = models.URLField(max_length=300, blank=False)

    # information to be scraped from flat add and stored in Landlords
    landlord_id = models.ForeignKey(
        Landlord,
        on_delete=models.CASCADE,
        blank=False)
