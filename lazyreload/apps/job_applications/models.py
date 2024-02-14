from django.db import models

# Create your models here.
class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=60, blank=False)
    company_website = models.URLField(max_length=250, blank=True)
    company_address = models.CharField(max_length=60, blank=True)
    company_mail = models.EmailField(max_length=60, blank=True)
    company_logo = models.ImageField(upload_to="logos", blank=True, null=True)
    company_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.company_name
    

class LazyJobApplication(models.Model):
    lazy_application_id = models.AutoField(primary_key=True)
    profile_id = models.ForeignKey(
        "users.LazyUserProfile",
        on_delete=models.CASCADE)
    add_link = models.URLField(max_length=250, blank=False)
    # information to be scraped from job ad
    company_id = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        blank=False)
    job_title = models.CharField(max_length=60, blank=False)
    job_ad_text = models.TextField()
    #additional manually filled information
    recruiter_name = models.CharField(max_length=60, blank=True)
    recruiter_mail = models.EmailField(max_length=60, blank=True)
    recruiter_phone = models.CharField(max_length=60, blank=True)
    # questions to the applicant
    JOB_TYPE_CHOICES = {
        "full": "Full Time",
        "part": "Part Time",
        "intern": "Internship",
        "free": "Freelance",
        "temp": "Temporary",
    }
    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES,
        default="full"
        )
    salary_expectation = models.IntegerField(blank=True, null=True)
    to_highlight = models.TextField(
        blank=True,
        verbose_name="Anything to highlight apart from CV Info?"
        )
    # application status
    APPLICANT_STATUS_CHOICES = {
        "apply": "Need to apply",
        "applied": "Applied",
        "interview": "Interview",
        "rejected": "Rejected",
        "accepted": "Accepted",
        "offer": "Offer",
        "hired": "Hired",
        "withdrawn": "Withdrawn",
    }
    application_send_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=APPLICANT_STATUS_CHOICES, default="apply")
    interview_date = models.DateField(blank=True, null=True)
    salary_offer = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)

    # ai settings
    # ai_settings = models.ForeignKey(
    #     "core.AiSettings",
    #     on_delete=models.CASCADE,
    #     blank=False
    # )
    # costs connected to the application
    application_costs = models.FloatField(blank=True, null=True)

