from rest_framework import serializers
from .models import LazyJobApplication, Company


class CompanySerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField(read_only=True)

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
    profile_id = serializers.IntegerField(read_only=True)
    add_link = serializers.URLField(max_length=250)
    job_type = serializers.CharField(max_length=60, default="full")
    salary_expectation = serializers.IntegerField(default=0)
    to_highlight = serializers.CharField(max_length=500, default="")
    company = CompanySerializer(required=False)

    class Meta:
        model = LazyJobApplication
        fields = (
            "add_link",
            "job_title"
            "job_type",
            "salary_expectation",
            "to_highlight",
            "job"      
     )


    def create(self, validated_data): 
        return LazyJobApplication.objects.create(**validated_data)


    def update(self, instance, validated_data):
        return LazyJobApplication.objects.update(**validated_data)
