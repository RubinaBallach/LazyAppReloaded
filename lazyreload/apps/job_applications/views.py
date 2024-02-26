from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .serializers import LazyJobApplicationSerializer, CompanySerializer
from .models import LazyJobApplication, Company
from apps.users.models import LazyUserProfile, LazyUser
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from apps.core.utils import CoverLetterGenerator
from .utils import JobAdImporter
from dotenv import load_dotenv
import os
from drf_multiple_model.views import ObjectMultipleModelAPIView
from django.http import JsonResponse



# Create your views here.
class LazyJobApplicationAPIView(ObjectMultipleModelAPIView):
    permission_classes = [IsAuthenticated]
    querylist = [
        {
            'queryset': LazyJobApplication.objects.all(),
            'serializer_class': LazyJobApplicationSerializer
        },
        {
            'queryset': Company.objects.all(),
            'serializer_class': CompanySerializer
        },
        {
            'queryset': LazyUserProfile.objects.all(),
        },
        {   'queryser': LazyUser.objects.all(),}
        ]

    @swagger_auto_schema(request_body=LazyJobApplicationSerializer, 
                         operation_description="Create a new job application",)
    def post(self, request):
        serializer = LazyJobApplicationSerializer(data=request.data)
        if serializer.is_valid():

            job_scraper = JobAdImporter(request.data["add_link"])
            info = job_scraper.retrieve_information()
            lazy_user = LazyUser.objects.get(username=request.user)
            lazy_user_profile = LazyUserProfile.objects.get(user=lazy_user)
            # Handle company creation/association:
            company, created = Company.objects.get_or_create(
                company_name=info["company_name"],
            )

            # Update/populate relevant company fields based on information from the job ad:
            if "company_website" in info:
                company.company_website = info["company_website"]
                company.save()
            if "company_location" in info:
                company.company_location = info["company_location"]
                company.save()
            if "company_mail" in info:
                company.company_mail = info["company_mail"]
                company.save()
            if "company_info" in info:
                company.company_info = info["company_info"]
                company.save()
            if "recruiter_name" in info:
                company.recruiter_name = info["recruiter_name"]
                company.save()
            if "recruiter_mail" in info:
                company.recruiter_mail = info["recruiter_mail"]
                company.save()
            if "recruiter_phone" in info:
                company.recruiter_phone = info["recruiter_phone"]
                company.save()
            
            # Save the LazyJobApplication with the associated company and user_profile:
            serializer.save(company_id=company, profile_id=lazy_user_profile)

            if not "salary_expectation" in request.data:
                salary_expectation = 0
                serializer.save(salary_expectation=salary_expectation)
            else:
                salary_expectation = request.data["salary_expectation"]
                serializer.save(salary_expectation=salary_expectation)
            if not "to_highlight" in request.data:
                to_highlight = ""
                serializer.save(to_highlight="")
            else:
                to_highlight = request.data["to_highlight"]
                serializer.save(to_highlight=to_highlight)
            if not "job_type" in request.data:
                job_type = "full"
                serializer.save(job_type="full")
            else:
                job_type = request.data["job_type"]
                serializer.save(job_type=job_type)
            if "job_title" in info:
                serializer.save(job_title=info["job_title"])
            if "job_ad_text" in info:
                job_description = info["job_ad_text"]
                serializer.save(job_ad_text=job_description)
            else:
                job_description = ""
                serializer.save(job_ad_text=job_description)

            # Generate a cover letter based on the job ad and the user's CV:
            load_dotenv()
            OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
            cover_letter_generator = CoverLetterGenerator(
                api_key=OPENAI_API_KEY,
                job_description=str(info),
                cv_extract=lazy_user_profile.cv_text,
                job_type=job_type,
                salary_expectation=salary_expectation,
                to_highlight=to_highlight
            )
            cover_letter = cover_letter_generator.generate_cover_letter()
            print(cover_letter)
            return JsonResponse(cover_letter, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
