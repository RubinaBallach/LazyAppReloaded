from rest_framework import serializers
from .models import LazyJobApplication, Company
from apps.users.models import LazyUserProfile, LazyUser
from apps.core.utils import CoverLetterGenerator
from .utils import JobAdImporter


class LazyJobApplicationSerializer(serializers.Serializer):
    model = LazyJobApplication
    fields = (
        "add_link",
        "job_title",
        "job_ad_text",        
    )

    
    
    # def create(self, validated_data):
    
    #     scraped_info = scrape_info.scrape_job_ad()
    #     job_ad_text = scraped_info["job_ad_text"]
    #     job_title = scraped_info["job_title"]
    #     return LazyJobApplication.objects.create(**validated_data)