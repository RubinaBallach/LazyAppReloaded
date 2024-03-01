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
from .utils import FlatApplicationGenerator

# Create views here

class LazyFlatApplicationView(APIView)
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
        #instantiate scrape flat information class









@api_view(['POST'])
def create_flat_application(request):
    serializer = FlatApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        
        # Generate flat application letter
        generator = FlatApplicationLetter(listing_info=serializer.validated_data['listing_info'], **serializer.validated_data)
        generated_flat_letter = generator.generate_flat_application_letter()

        # Update the FlatApplication instance with the generated letter
        flat_application_instance = FlatApplication.objects.get(pk=serializer.data['id'])
        flat_application_instance.generated_letter = generated_flat_letter
        flat_application_instance.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_flat_listing(request):
    serializer = FlatListingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def display_generated_letters(request):
    flat_applications = FlatApplication.objects.all()
    return render(request, 'generated_letters.html', {'flat_applications': flat_applications})
