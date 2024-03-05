import os
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from dotenv import load_dotenv
from django.http import JsonResponse
from .models import LazyFlatApplication, LazyRenter, Landlord
from .serializers import LandlordSerializer, LazyRenterSerializer, LazyFlatApplicationSerializer
from .utils import FlatAdImporter, FlatApplicationLetterGenerator
from apps.users.models import LazyUser, LazyUserProfile

# Create views here
class LazyRenterAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LazyRenterSerializer
    queryset = LazyRenter.objects.all()
  
    @swagger_auto_schema(operation_description="Retrieve renter profile",
                         request_body=LazyRenterSerializer)
    def get_object(self):
        lazyrenter, created = LazyRenter.objects.get_or_create(
            profile_id=self.request.profile_id)
        return lazyrenter
   
    @swagger_auto_schema(operation_description="Create renter profile",
                         request_body=LazyRenterSerializer)
    def post(self, request):
        # Get LazyUser and LazyUserProfile instances to link with LazyRenter
        lazy_user = LazyUser.objects.get(username=request.user)
        lazy_user_profile = LazyUserProfile.objects.get(user=lazy_user)
        lazy_renter, created = LazyRenter.objects.get_or_create(
            profile_id=lazy_user_profile)
     
        if not created:
            return JsonResponse({'detail': 'Renter profile already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    
        if 'first_name' not in request.data:
            lazy_renter.first_name = lazy_user.first_name
        if 'last_name' not in request.data:
            lazy_renter.last_name = lazy_user.last_name
        if 'email' not in request.data:
            lazy_renter.email = lazy_user.email
        serializer = LazyRenterSerializer(lazy_renter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    @swagger_auto_schema(operation_description="Retrieve renter profile",
                         request_body=LazyRenterSerializer)
    def get(self, request):
        if "renter_id" in request.data:
            try:
                lazyrenter = LazyRenter.objects.get(renter_id=request.data["renter_id"])
            except LazyRenter.DoesNotExist:
                return JsonResponse({'detail': 'Renter not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            lazy_user = LazyUser.objects.get(username=request.user)
            lazy_user_profile = LazyUserProfile.objects.get(user=lazy_user)
            print(lazy_user.username)
            try:
                lazyrenter = LazyRenter.objects.get(profile_id=lazy_user_profile)
            except LazyRenter.DoesNotExist:
                return JsonResponse({'detail': f'Renter Profile for {lazy_user.username} not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LazyRenterSerializer(lazyrenter)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Update renter profile",
                         request_body=LazyRenterSerializer)
    def put(self, request):
        if "renter_id" in request.data:
            try:
                lazyrenter = LazyRenter.objects.get(renter_id=request.data["renter_id"])
            except LazyRenter.DoesNotExist:
                return Response({'detail': 'Renter Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            lazy_user = LazyUser.objects.get(username=request.user)
            lazy_user_profile = LazyUserProfile.objects.get(user=lazy_user)
            try:
                lazyrenter = LazyRenter.objects.get(profile_id=lazy_user_profile)
            except LazyRenter.DoesNotExist:
                return JsonResponse({'detail': f'Renter Profile for {lazy_user.username} not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LazyRenterSerializer(lazyrenter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
      
    @swagger_auto_schema(operation_description="Delete renter profile",
                            request_body=LazyRenterSerializer)
    def delete(self, request):
        if "renter_id" in request.data:
            try:
                lazyrenter = LazyRenter.objects.get(renter_id=request.data["renter_id"])
            except LazyRenter.DoesNotExist:
                return Response({'detail': 'Renter Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
            lazyrenter.delete()
            return JsonResponse({'detail': 'Renter deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({'detail': 'Renter ID not provided.'}, status=status.HTTP_400_BAD_REQUEST)

class LandlordAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LandlordSerializer
    queryset = Landlord.objects.all()
    
    @swagger_auto_schema(operation_description="Retrieve landlord profile",
                         request_body=LandlordSerializer)
    def get(self, request):
        if "landlord_id" in request.data:
            try:
                landlord = Landlord.objects.get(landlord_id=request.data["landlord_id"])
            except Landlord.DoesNotExist:
                return JsonResponse({'detail': 'Landlord not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'detail': 'Landlord ID not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = LandlordSerializer(landlord)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_description="Create landlord profile",
                         request_body=LandlordSerializer)
    def post(self, request):
        landlord, created = Landlord.objects.get_or_create(
            landlord_id=request.data['landlord_id'])
        if not created:
            return JsonResponse({'detail': 'Landlord profile already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = LandlordSerializer(landlord, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(operation_description="Update landlord profile",
                            request_body=LandlordSerializer)
    def put(self, request):
        if "landlord_id" in request.data:
            try:
                landlord = Landlord.objects.get(landlord_id=request.data["landlord_id"])
            except Landlord.DoesNotExist:
                return Response({'detail': 'Landlord not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'detail': 'Landlord ID not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = LandlordSerializer(landlord, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        
    @swagger_auto_schema(operation_description="Delete landlord profile",   
                            request_body=LandlordSerializer)
    def delete(self, request):
        if "landlord_id" in request.data:
            try:
                landlord = Landlord.objects.get(landlord_id=request.data["landlord_id"])
            except Landlord.DoesNotExist:
                return Response({'detail': 'Landlord not found.'}, status=status.HTTP_404_NOT_FOUND)
            landlord.delete()
            return JsonResponse({'detail': 'Landlord deleted successfully'}, status=status.HTTP_204_NO_CONTENT) 


class LazyFlatApplicationAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LazyFlatApplicationSerializer
    queryset = LazyFlatApplication.objects.all()

    @swagger_auto_schema(operation_description="Retirieve flat application",
                         request_body=LazyFlatApplicationSerializer)
    def get_object(self):
        flat_application, created = LazyFlatApplication.objects.get_or_create(
            flat_application_id=self.request.flat_application_id)
        return flat_application
    
    @swagger_auto_schema(operation_description="Create flat application",
                         request_body=LazyFlatApplicationSerializer)
    def post(self, request):
        # instantiate scrape flat information class
        flat_ad_info = FlatAdImporter(request.data['flat_ad_link']).retrieve_information()
        print(flat_ad_info)




