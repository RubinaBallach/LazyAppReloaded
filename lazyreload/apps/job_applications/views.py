from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import LazyJobApplicationSerializer
from .models import LazyJobApplication, Company
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from apps.core.utils import CoverLetterGenerator
from .utils import JobAdImporter

import requests


# Create your views here.
class LazyJobApplicationView(CreateAPIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = LazyJobApplicationSerializer

    # @swagger_auto_schema(
    #     request_body=LazyJobApplicationSerializer,
    #     operation_description="Create a new job application",
    #     operation_summary="Create a new job application",
    #     responses={201: "Created"}
    # )
    def post(self, request):
        print(request.data)
        job_scraper = JobAdImporter(request.data["add_link"])
        info = job_scraper.retrieve_information()
        print(info)

        return Response(status=status.HTTP_201_CREATED)
       