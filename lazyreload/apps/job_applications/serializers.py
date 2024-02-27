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
    add_link = serializers.URLField(max_length=250)
    job_type = serializers.CharField(max_length=60, default="full")
    salary_expectation = serializers.IntegerField(default=0)
    to_highlight = serializers.CharField(max_length=500, default="")
    company = CompanySerializer(required=False)

    class Meta:
        model = LazyJobApplication
        fields = (
            "add_link",
            "job_type",
            "salary_expectation",
            "to_highlight",      
     )


    def create(self, validated_data): 
        return LazyJobApplication.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.add_link = validated_data.get("add_link", instance.add_link)
        instance.job_type = validated_data.get("job_type", instance.job_type)
        instance.salary_expectation = validated_data.get("salary_expectation", instance.salary_expectation)
        instance.to_highlight = validated_data.get("to_highlight", instance.to_highlight)
        instance.save()
        return instance
        
    