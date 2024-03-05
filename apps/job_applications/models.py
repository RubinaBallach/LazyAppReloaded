from django.db import models

# Create your models here.
class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=60, blank=False)
    company_website = models.URLField(max_length=250, blank=True)
    company_location = models.CharField(max_length=60, blank=True)
    company_mail = models.EmailField(max_length=60, blank=True)
    company_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.company_name


STATUS_CHOICES = (
    
    ("pending", "Pending"),
    ("accepted", "Accepted"),
    ("rejected", "Rejected"),
    
)

class LazyJobApplication(models.Model):
    lazy_application_id = models.AutoField(primary_key=True)
    profile_id = models.ForeignKey(
        "users.LazyUserProfile",
        on_delete=models.CASCADE, blank=True, null=True)
    ad_link = models.URLField(max_length=250, blank=False)
    # information to be scraped from job ad
    company_id = models.ForeignKey(
        Company,
        on_delete=models.CASCADE, blank=True, null=True)
    job_title = models.CharField(max_length=250, blank=False)
    job_ad_text = models.TextField()
    # additional manually filled information
    recruiter_name = models.CharField(max_length=60, blank=True)
    recruiter_mail = models.EmailField(max_length=60, blank=True)
    recruiter_phone = models.CharField(max_length=60, blank=True)
    # questions to the applicant
    JOB_TYPE_CHOICES = [
        ("full", "Full Time"),
        ("part", "Part Time"),
        ("intern", "Internship"),
        ("free", "Freelance"),
        ("temp", "Temporary"),
    ]
    job_type = models.CharField(
        max_length=60,
        choices=JOB_TYPE_CHOICES,
        default="full"
        )
    salary_expectation = models.IntegerField(blank=True, null=True)
    to_highlight = models.TextField(
        blank=True, null=True,
        verbose_name="Anything to highlight apart from CV Info?"
        )
    # application status 
    APPLICANT_STATUS_CHOICES = [
        ("apply", "Need to apply"),
        ("applied", "Applied"),
        ("interview", "Interview"),
        ("rejected", "Rejected"),
        ("accepted", "Accepted"),
        ("offer", "Offer"),
        ("hired", "Hired"),
        ("withdrawn", "Withdrawn"),
    ]
    

    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=APPLICANT_STATUS_CHOICES, default="apply")
    application_send_date = models.DateField(blank=True, null=True)
    interview_date = models.DateField(blank=True, null=True)
    salary_offer = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    application_costs = models.FloatField(blank=True, null=True)


