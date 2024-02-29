from rest_framework import serializers
from .models import LazyJobApplication, Company
from apps.users.models import LazyUserProfile


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
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
    job_type = serializers.CharField(max_length=60, default="full")
    job_title = serializers.CharField(max_length=60, required=False)
    job_ad_text = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)
    recruiter_name = serializers.CharField(max_length=250, required=False)
    recruiter_mail = serializers.EmailField(max_length=60, required=False)
    recruiter_phone = serializers.CharField(max_length=60, required=False)
    cover_letter = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)

    company_id = serializers.PrimaryKeyRelatedField(required=False, queryset=Company.objects.all())
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
    

