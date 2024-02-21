from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import LazyJobApplicationSerializer, CompanySerializer
from .models import LazyJobApplication, Company
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
import requests


# Create your views here.
class LazyJobApplicationView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LazyJobApplicationSerializer

    @swagger_auto_schema(
        request_body=LazyJobApplicationSerializer,
        operation_description="Create a new job application",
        operation_summary="Create a new job application",
        responses={201: "Created"}
    )
    def post(self, request):
        serializer = LazyJobApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)