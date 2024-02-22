from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import LazyJobApplicationSerializer, CompanySerializer
from .models import LazyJobApplication, Company
from apps.users.models import LazyUserProfile, LazyUser
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from apps.core.utils import CoverLetterGenerator
from .utils import JobAdImporter
from dotenv import load_dotenv
from drf_multiple_model.views import ObjectMultipleModelAPIView



# Create your views here.
class LazyJobApplicationAPIView(ObjectMultipleModelAPIView):
    permission_classes = [IsAuthenticated]
    querylist =[
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

    # @swagger_auto_schema(
    #     request_body=LazyJobApplicationSerializer,
    #     operation_description="Create a new job application",
    #     operation_summary="Create a new job application",
    #     responses={201: "Created"}
    # )
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
            print(info)

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

            if "job_title" in info:
                serializer.save(job_title=info["job_title"])
            if "job_ad_text" in info:
                serializer.save(job_ad_text=info["job_ad_text"])
        
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       