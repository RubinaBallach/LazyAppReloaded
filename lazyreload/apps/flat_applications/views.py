

from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import FlatApplication, FlatListing
from .serializers import FlatApplicationSerializer, FlatListingSerializer
from .flat_application_letter_generator import FlatApplicationLetter  # Assuming you have this module

# Create views here
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
