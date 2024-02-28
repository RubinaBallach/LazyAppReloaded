from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
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
from django.http import HttpRequest, HttpResponse, JsonResponse



# Create your views here.
class LazyJobApplicationAPIView(ObjectMultipleModelAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LazyJobApplicationSerializer
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
        {   'queryset': LazyUser.objects.all(),}
        ]

    @swagger_auto_schema(operation_description="Retrieve job application",request_body=LazyJobApplicationSerializer)
    def get_object(self):
        job_application, created = LazyJobApplication.objects.get_or_create(lazy_application_id=self.request.lazy_application_id)
        return job_application

    @swagger_auto_schema(request_body=LazyJobApplicationSerializer, 
                         operation_description="Create a new job application",)
    def post(self, request):
        # instantiate scrape job information class
        job_scraper = JobAdImporter(request.data["ad_link"])
        info = job_scraper.retrieve_information()
        # Get the LazyUser and LazyUserProfile associated with the request:
        lazy_user = LazyUser.objects.get(username=request.user)
        lazy_user_profile = LazyUserProfile.objects.get(user=lazy_user)
        # Handle company creation/association:
        company, created = Company.objects.get_or_create(
            company_name=info["company_name"],
        )
        company_serializer = CompanySerializer(company, data=request.data, partial=True)
        # Handle JobApplication creation/association:
        job_application = LazyJobApplication.objects.get_or_create(company_id=company, profile_id=lazy_user_profile)
        job_application_serializer = LazyJobApplicationSerializer(job_application, data=request.data, partial=True)
        job_application_serializer.is_valid(raise_exception=True)

        if company_serializer.is_valid:
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
        
        if job_application_serializer.is_valid:
            # user input salary expectation
            salary_expectation = request.data["salary_expectation"] if "salary_expectation" in request.data else 0
            job_application_serializer.save(salary_expectation=salary_expectation)
            # user input special things to highlight
            to_highlight = request.data["to_highlight"] if "to_highlight" in request.data else ""
            job_application_serializer.save(to_highlight=to_highlight)
            # user input job type (full, part, intern, freelance, temporary)
            job_type = request.data["job_type"] if "job_type" in request.data else "full"
            job_application_serializer.save(job_type=job_type)
            # scraped data from job ad
            job_title = info["job_title"] if "job_title" in info else ""
            job_application_serializer.save(job_title = job_title)
            job_ad_text = info["job_description"] if "job_description" in info else ""
            job_application_serializer.save(job_ad_text=job_ad_text)

        # Generate a cover letter based on the job ad and the user's CV:
        load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        cover_letter_generator = CoverLetterGenerator(
            api_key=OPENAI_API_KEY,
            job_description=str(info),
            cv_extract=lazy_user_profile.cv_text,
            job_type=job_type,
            salary_expectation=salary_expectation,
            to_highlight=to_highlight,
            availability = lazy_user_profile.availability,
        )
        cover_letter = cover_letter_generator.generate_cover_letter()
        job_application_serializer.save(cover_letter=cover_letter)
        return JsonResponse(cover_letter, status=status.HTTP_201_CREATED, safe=False)

    @swagger_auto_schema(operation_description="Retrieve a job application", request_body=LazyJobApplicationSerializer)
    def get(self, request):
        """Get a specific job application or all job applications."""
        if "lazy_application_id" in request.data:
            # Retrieve a specific job application
            try:
                job_application = LazyJobApplication.objects.filter(lazy_application_id=request.data["lazy_application_id"]).select_related('company').get()
            except LazyJobApplication.DoesNotExist:
                # Handle case where object is not found 
                return JsonResponse("Job application does not exist", status=status.HTTP_404_NOT_FOUND, safe=False)
            serializer = LazyJobApplicationSerializer(job_application)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        else:
            # Retrieve all job applications
            job_applications = LazyJobApplication.objects.all()
            serializer = LazyJobApplicationSerializer(job_applications, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        
    def put(self, request):
        """Update a job application."""
        if "lazy_application_id" in request.data:
            # Retrieve the job application to be updated
            try:
                job_application = LazyJobApplication.objects.get(lazy_application_id=request.data["lazy_application_id"])
            except LazyJobApplication.DoesNotExist:
                return JsonResponse("The Job application you would like to update does not exist.", status=status.HTTP_404_NOT_FOUND, safe=False)
            serializer = LazyJobApplicationSerializer(job_application, data=request.data, partial=True)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse("You need to provide a job application id to update a job application.", status=status.HTTP_400_BAD_REQUEST, safe=False)




