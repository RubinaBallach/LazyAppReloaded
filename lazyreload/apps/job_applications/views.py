from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, ListAPIView
from .serializers import LazyJobApplicationSerializer, CompanySerializer
from .models import LazyJobApplication, Company
from apps.users.models import LazyUserProfile, LazyUser
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from apps.core.utils import CoverLetterGenerator
from .utils import JobAdImporter
from dotenv import load_dotenv
import os
from django.http import HttpRequest, HttpResponse, JsonResponse



# Create your views here.
class LazyJobApplicationAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LazyJobApplicationSerializer
    queryset = LazyJobApplication.objects.all()

    @swagger_auto_schema(operation_description="Retrieve job application",request_body=LazyJobApplicationSerializer)
    def get_object(self):
        job_application, created = LazyJobApplication.objects.get_or_create(lazy_application_id=self.request.lazy_application_id)
        return job_application

    @swagger_auto_schema(request_body=LazyJobApplicationSerializer, 
                         operation_description="Create a new job application",)
    def post(self, request):
        # instantiate scrape job information class
        try:
            job_scraper = JobAdImporter(request.data["ad_link"])
            info = job_scraper.retrieve_information()
        except Exception as e:
            print(f"Error scraping job information: {e}")
            return JsonResponse(
                {"error": "Failed to scrape job information"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                safe=False,
            )
        # Get the LazyUser and LazyUserProfile associated with the request:
        lazy_user = LazyUser.objects.get(username=request.user)
        lazy_user_profile = LazyUserProfile.objects.get(user=lazy_user)
        # Handle company creation/association:
        company, created = Company.objects.get_or_create(company_name=info["company_name"],
        )
        if not created:
            # Update or create company information
            company.company_website = info.get("company_website", company.company_website)
            company.company_location = info.get("company_location", company.company_location)
            company.company_mail = info.get("company_mail", company.company_mail)
            company.company_info = info.get("company_info", company.company_info)
            company.save()

        # Create job application:
        job_application, created = LazyJobApplication.objects.get_or_create(
            company_id=company, profile_id=lazy_user_profile, ad_link=request.data["ad_link"]
            )
        serializer = LazyJobApplicationSerializer(job_application, data=request.data)
        serializer.is_valid(raise_exception=True)
        # prepare data for serializer
        data ={
            "profile_id": lazy_user_profile.lazy_user_id,
            "salary_expectation": request.data.get("salary_expectation",0),
            "to_highlight": request.data.get("to_highlight",""),
            "job_type": request.data.get("job_type","full"),
            "job_title": info.get("job_title",0),
            "job_ad_text": info.get("job_description",0),
            "recruiter_name": info.get("recruiter_name",""),
            "recruiter_mail": info.get("recruiter_mail",""),
            "recruiter_phone": info.get("recruiter_phone","")
        
        }
        
        # Generate a cover letter based on the job ad and the user's CV:
        try:
            # load_dotenv()
            # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
            # cover_letter = CoverLetterGenerator(
            #     api_key=OPENAI_API_KEY,
            #     job_description=str(info),
            #     cv_extract=lazy_user_profile.cv_text,
            #     job_type=data["job_type"],
            #     salary_expectation=data["salary_expectation"],
            #     to_highlight=data["to_highlight"],
            #     availability = lazy_user_profile.availability,
            # ).generate_cover_letter()
            # data["cover_letter"] = cover_letter
            serializer.save(**data) # save all data at once
        except Exception as e:  # Catch potential errors during cover letter generation
            print(f"Error generating cover letter: {e}")
            return JsonResponse(
                {"error": "Failed to generate cover letter"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                safe=False)    
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)

    @swagger_auto_schema(operation_description="Retrieve a job application", request_body=LazyJobApplicationSerializer)
    def get(self, request):
        """Get a specific job application or all job applications."""
        if "lazy_application_id" in request.data:
            # Retrieve a specific job application
            try:
                job_application = LazyJobApplication.objects.filter(lazy_application_id=request.data["lazy_application_id"]).select_related("company_id").get()
            except LazyJobApplication.DoesNotExist:
                # Handle case where object is not found 
                return JsonResponse("Job application does not exist", status=status.HTTP_404_NOT_FOUND, safe=False)
            serializer = LazyJobApplicationSerializer(job_application)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse("You need to provide a job application id to see a job application.", status=status.HTTP_400_BAD_REQUEST, safe=False)
        
    @swagger_auto_schema(operation_description="Update a job application", request_body=LazyJobApplicationSerializer)    
    def put(self, request):
        """Update a job application."""
        if "lazy_application_id" in request.data:
            # Retrieve the job application to be updated
            try:
                 job_application = LazyJobApplication.objects.filter(lazy_application_id=request.data["lazy_application_id"]).select_related("company_id").get()
            except LazyJobApplication.DoesNotExist:
                return JsonResponse("The Job application you would like to update does not exist.", status=status.HTTP_404_NOT_FOUND, safe=False)
            # Handle company update (if provided):
            company_data = request.data.get("company", None)

            # Validate and update data
            serializer = LazyJobApplicationSerializer(job_application, data=request.data, partial=True, company_data=company_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False),
            else:
                # Handle validation errors
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)
        else:
            return JsonResponse("You need to provide a job application id to update a job application.", status=status.HTTP_400_BAD_REQUEST, safe=False)


class JobApplicationListAPIView(ListAPIView):
    pass

class CompanyAPIView(APIView):
    pass

class ComapnyListAPIView(ListAPIView):
    pass
