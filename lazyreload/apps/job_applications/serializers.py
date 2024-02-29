from rest_framework import serializers
from .models import LazyJobApplication, Company
from apps.users.models import LazyUserProfile

JOB_TYPE_CHOICES = [
        ("full", "Full Time"),
        ("part", "Part Time"),
        ("intern", "Internship"),
        ("free", "Freelance"),
        ("temp", "Temporary"),
    ]
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
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "company_id",
            "company_name",
            "company_website",
            "company_location",
            "company_mail",
            "company_info",
        )

class LazyJobApplicationSerializer(serializers.Serializer):
    lazy_application_id = serializers.IntegerField(read_only=True)
    profile_id = serializers.PrimaryKeyRelatedField(read_only=True)
    ad_link = serializers.URLField(max_length=200)
    salary_expectation = serializers.IntegerField(default=0)
    to_highlight = serializers.CharField(style={'base_template': 'textarea.html'}, required=False, default="")
    job_type = serializers.ChoiceField(choices=JOB_TYPE_CHOICES, default="full")
    job_title = serializers.CharField(max_length=60, required=False)
    job_ad_text = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)
    recruiter_name = serializers.CharField(max_length=250, required=False)
    recruiter_mail = serializers.EmailField(max_length=60, required=False)
    recruiter_phone = serializers.CharField(max_length=60, required=False)
    cover_letter = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)
    application_costs = serializers.FloatField(read_only=True)

    #company_id = serializers.PrimaryKeyRelatedField(required=False, queryset=Company.objects.all())
    company= CompanySerializer(source="company_id", read_only=True)


    class Meta:
        model = LazyJobApplication
        fields = (
            "lazy_application_id",
            "profile_id",
            "ad_link",
            "salary_expectation",
            "to_highlight",
            "job_type",
            "job_title",
            "job_ad_text",
            "recruiter_name",
            "recruiter_mail",
            "recruiter_phone",
            "cover_letter",
            "company_id",
            "company",
     )
    

    def create(self, validated_data): 
        return LazyJobApplication.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.ad_link = validated_data.get("ad_link", instance.ad_link)
        instance.salary_expectation = validated_data.get("salary_expectation", instance.salary_expectation)
        instance.to_highlight = validated_data.get("to_highlight", instance.to_highlight)
        instance.job_type = validated_data.get("job_type", instance.job_type)
        instance.job_title = validated_data.get("job_title", instance.job_title)
        instance.job_ad_text = validated_data.get("job_ad_text", instance.job_ad_text)
        instance.recruiter_name = validated_data.get("recruiter_name", instance.recruiter_name)
        instance.recruiter_mail = validated_data.get("recruiter_mail", instance.recruiter_mail)
        instance.recruiter_phone = validated_data.get("recruiter_phone", instance.recruiter_phone)
        instance.cover_letter = validated_data.get("cover_letter", instance.cover_letter)
        instance.company_id = validated_data.get("company_id", instance.company_id)
        # Handle company update (if provided):
        company_data = validated_data.get("company", None)
        if company_data:
            # Check if company exists and update if necessary
            try:
                company, created = Company.objects.get_or_create(
                    company_name=company_data.get("company_name", instance.company.company_name)
                )
                if not created:
                    # Update existing company fields (optional)
                    company.company_website = company_data.get("company_website", company.company_website)
                    company.company_location = company_data.get("company_location", company.company_location)
                    company.company_mail = company_data.get("company_mail", company.company_mail)
                    company.company_info = company_data.get("company_info", company.company_info)
                    company.save()
                # Update the job application's company association
                instance.company = company
            except KeyError:  # Handle cases where "company_name" is missing in the data
                return JsonResponse(
                    {"error": "Missing company_name in the company data"},
                    status=status.HTTP_400_BAD_REQUEST,
                    safe=False,
                )
        instance.save()
        return instance
    

class LazyJobApplicationDashboardSerializer(serializers.Serializer):
    """Serializer class used to display and updated the status of a job application."""
    lazy_application_id = serializers.IntegerField(read_only=True)
    profile_id = serializers.PrimaryKeyRelatedField(read_only=True)
    ad_link = serializers.URLField(max_length=200, read_only=True)
    salary_expectation = serializers.IntegerField(default=0)
    job_type = serializers.ChoiceField(choices=JOB_TYPE_CHOICES, read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(required=False, queryset=Company.objects.all())
    company_name= serializers.CharField(source="company_id.company_name", read_only=True)
    job_title = serializers.CharField(max_length=60, read_only=True)
    recruiter_name = serializers.CharField(max_length=250, required=False)
    recruiter_mail = serializers.EmailField(max_length=60, required=False)
    recruiter_phone = serializers.CharField(max_length=60, required=False)
    status = serializers.ChoiceField(choices=APPLICANT_STATUS_CHOICES, default="apply")
    application_send_date = serializers.DateTimeField(required=False)
    interview_date = serializers.DateTimeField(required=False)
    salary_offer = serializers.IntegerField(required=False)
    start_date = serializers.DateTimeField(required=False)
    notes = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)
    application_costs = serializers.FloatField(read_only=True)

    class Meta:
        model = LazyJobApplication
        fields = ("__all__")

    def update(self, instance, validated_data):
        instance.salary_expectation = validated_data.get("salary_expectation", instance.salary_expectation)
        instance.recruiter_name = validated_data.get("recruiter_name", instance.recruiter_name)
        instance.recruiter_mail = validated_data.get("recruiter_mail", instance.recruiter_mail)
        instance.recruiter_phone = validated_data.get("recruiter_phone", instance.recruiter_phone)
        instance.status = validated_data.get("status", instance.status)
        instance.application_send_date = validated_data.get("application_send_date", instance.application_send_date)
        instance.interview_date = validated_data.get("interview_date", instance.interview_date)
        instance.salary_offer = validated_data.get("salary_offer", instance.salary_offer)
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.save()
        return instance