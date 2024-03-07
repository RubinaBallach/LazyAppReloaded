from django.db import models


class Landlord(models.Model):
    landlord_id = models.AutoField(primary_key=True)
    landlord_name = models.CharField(max_length=60, blank=True)
    landlord_contact = models.EmailField(max_length=60, blank=True)
    landlord_address = models.CharField(max_length=60, blank=True)
    landlord_phone = models.CharField(max_length=60, blank=True)
    landlord_notes = models.TextField(blank=True)

class LazyRenter(models.Model):
    renter_id = models.AutoField(primary_key=True)
    profile_id = models.ForeignKey(
        "users.LazyUserProfile",
        on_delete=models.CASCADE)
    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    renter_mail = models.EmailField(max_length=60, blank=True)
    renter_phone = models.CharField(max_length=60, blank=True)
    current_address = models.TextField(blank=True)
    current_occupation = models.CharField(max_length=60, blank=True)
    net_income = models.IntegerField(blank=True,
                                     null=True,
                                     verbose_name="Net Income per month"
                                     )
    stable_income_available = models.BooleanField(default=False)
    guarantee_available = models.BooleanField(default=False)
    clean_schufa_report = models.BooleanField(default=False)
    references_available = models.BooleanField(default=False)
    long_term_leasing_desire = models.BooleanField(default=True)
    quiet_and_tidy_tenant = models.BooleanField(default=True)
    pets = models.BooleanField(default=False)
    type_of_pets = models.CharField(max_length=60, blank=True)
    no_of_people = models.IntegerField(blank=True,
                                       null=True,
                                       verbose_name="Number of People to move"
                                       )
    children = models.BooleanField(default=False)
    no_of_children = models.IntegerField(verbose_name="No. of children", default=0)
    
    def save(self, *args, **kwargs):
        if not self.renter_mail:
            self.renter_mail = self.profile_id.email
        if self.children == False:
            self.no_of_children = 0
        super(LazyRenter, self).save(*args, **kwargs)


class LazyFlatApplication(models.Model):
    flat_application_id = models.AutoField(primary_key=True)
    renter_id = models.ForeignKey(
        LazyRenter,
        on_delete=models.CASCADE)
    landlord_id = models.ForeignKey(
        Landlord,
        on_delete=models.CASCADE,
        blank=False)
    # information to be scraped from flat add and stored in Landlords
    flat_ad_link = models.URLField(max_length=300, blank=False)
    title = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=50, blank=False)
    postal_code = models.IntegerField(blank=True, null=True)
    district = models.CharField(max_length=50, blank=False)
    kaltmiete = models.CharField(max_length=20, blank=False)
    apartment_size = models.CharField(max_length=20, blank=False)
    deposit = models.CharField(max_length=20, blank=True)
    rooms = models.IntegerField(blank=True, null=True)
    extra_costs = models.CharField(max_length=20, blank=True)
    heating_costs = models.CharField(max_length=100, blank=True)
    total_cost = models.CharField(max_length=20, blank=False)

    additional_notes = models.TextField(blank=True)
    flat_application_letter = models.TextField(blank=True)


    def __str__(self):
        return f"{self.title} in {self.city}, {self.district}"