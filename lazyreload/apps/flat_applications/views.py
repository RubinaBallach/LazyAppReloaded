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
from .serializers import LandlordSerializer, LazyRenterSerializer, LazyFlatApplicationSerializer, LazyFlatApplicationDashboardSerializer
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
        try:
            flat_ad_importer = FlatAdImporter(request.data['flat_ad_link'])
            flat_info = flat_ad_importer.retrieve_information()
        except Exception as e:
            print(f"Erro retrieving job information: {e}")
            return JsonResponse(
                {"error": "Error retrieving flat information"},
                status=status.HTTP_400_BAD_REQUEST,
                safe=False,
            )
        # Get LazyUser and LazyUserProfile instances associated with the request:
        lazy_user = LazyUser.objects.get(username=request.user)
        lazy_user_profile = LazyUserProfile.objects.get(user=lazy_user)
        # Get LazyRenter instance
        lazy_renter = LazyRenter.objects.get(profile_id=lazy_user_profile)

        # Get Landlord instance or create if not exists
        landlord, created = Landlord.objects.get_or_create(
            landlord_name=flat_info['landlord_name'])
        landlord_data = {}
        if created:
            landlord_data["landlord_address"] = flat_info.get('landlord_address', "Address not found")
            landlord_data["landlord_contact"] = flat_info.get('landlord_contact', "Contact not found")
        else:
            landlord_data["landlord_address"] = flat_info.get('landlord_address', landlord.landlord_address)
            landlord_data["landlord_contact"] = flat_info.get('landlord_contact', landlord.landlord_contact)
        landlord_serializer = LandlordSerializer(data=landlord_data)
        landlord_serializer.is_valid(raise_exception=True)
        landlord_serializer.save()
        landlord_data["landlord_name"] = flat_info['landlord_name']

        # Create flat application - gather data to pass to Generator function
        flat_application=LazyFlatApplication.objects.create(
            renter_id=lazy_renter,
            landlord_id=landlord,
            flat_ad_link=request.data['flat_ad_link']
        )
        flat_application_data = {
            "renter_id": lazy_renter,
            "landlord_id": landlord,
            "title": flat_info.get('title', "Title not found"),
            "city": flat_info.get('city', "City not found"),
            "postal_code": flat_info.get('postal_code', "Postal code not found"),
            "district": flat_info.get('district', "District not found"),
            "kaltmiete": flat_info.get('kaltmiete', "Kaltmiete not found"),
            "deposit": flat_info.get('deposit', "Deposit not found"),
            "apartment_size":flat_info.get('apartment_size'),
            "rooms": flat_info.get('rooms', "Rooms not found"),
            "extra_costs": flat_info.get('extra_costs', "Extra costs not found"),
            "heating_costs": flat_info.get('heating_costs', "Heating costs not found"),
            "total_cost": flat_info.get('total_cost', "Total cost not found"),
            "additional_notes": flat_info.get('additional_notes', "no additional notes found"),
        }
        flat_application_serializer = LazyFlatApplicationSerializer(flat_application, data=flat_application_data )

        lazy_renter_data = {
            "first_name": lazy_renter.first_name, 
            "last_name": lazy_renter.last_name,
            "date_of_birth": lazy_renter.date_of_birth,
            "renter_mail": lazy_renter.renter_mail,
            "renter_phone": lazy_renter.renter_phone,
            "current_address": lazy_renter.current_address,
            "current_occupation": lazy_renter.current_occupation,
            "net_income": lazy_renter.net_income,
            "stable_income_available": lazy_renter.stable_income_available,
            "guarantee_available": lazy_renter.guarantee_available,
            "clean_schufa_report": lazy_renter.clean_schufa_report,
            "references_available": lazy_renter.references_available,
            "long_term_leasing_desire": lazy_renter.long_term_leasing_desire,
            "quiet_and_tidy_tenant": lazy_renter.quiet_and_tidy_tenant,
            "pets": lazy_renter.pets,
            "type_of_pets": lazy_renter.type_of_pets,
            "no_of_people": lazy_renter.no_of_people,
            "children": lazy_renter.children,
            "no_of_children": lazy_renter.no_of_children,
        }
        # Generate flat application letter
        try:
            load_dotenv()
            OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
            flat_app_letter_gen = FlatApplicationLetterGenerator(
                api_key=OPENAI_API_KEY,
                flat_application_data=flat_application_data,
                lazy_renter_data=lazy_renter_data,
                landlord_data=landlord_data)
        
            flat_application_data["flat_application_letter"] = flat_app_letter_gen.generate_flat_application_letter()
        except Exception:  # catch potential errors during application letter generation
             return JsonResponse(
                 {"error": "Failed to generate application letter"},
                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                 safe=False
             )

        flat_application_serializer.is_valid(raise_exception=True)
        flat_application_serializer.save(**flat_application_data)
        return JsonResponse(flat_application_serializer.data,
            status=status.HTTP_201_CREATED, safe=False)

    @swagger_auto_schema(operation_description="Retrieve flat application",
                            request_body=LazyFlatApplicationSerializer)
    def get(self, request):
        """Retrieve specfic flat applications or all flat applications"""
        if "flat_application_id" in request.data:
            try:
                flat_application = LazyFlatApplication.objects.get(flat_application_id=request.data["flat_application_id"])
            except LazyFlatApplication.DoesNotExist:
                return JsonResponse({'detail': 'Flat Application not found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = LazyFlatApplicationSerializer(flat_application)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            flat_applications = LazyFlatApplication.objects.all()
            serializer = LazyFlatApplicationSerializer(flat_applications, many=True)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
     
    @swagger_auto_schema(operation_description="Update flat application",
                            request_body=LazyFlatApplicationSerializer)
    def put(self, request):
        """Update flat application"""
        if "flat_application_id" in request.data:
            try:
                flat_application = LazyFlatApplication.objects.get(flat_application_id=request.data["flat_application_id"]).select_related('renter_id', 'landlord_id')
            except LazyFlatApplication.DoesNotExist:
                return JsonResponse("The flat application does not exist.", status=status.HTTP_404_NOT_FOUND, safe=False)
            serializer = LazyFlatApplicationSerializer(flat_application, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)
        else:
            return JsonResponse('Flat Application ID not provided.', status=status.HTTP_400_BAD_REQUEST, safe=False)

    @swagger_auto_schema(operation_description="Delete flat application",
                            request_body=LazyFlatApplicationSerializer)  
    def delete(self, request):
        """Delete flat application"""
        if "flat_application_id" in request.data:
            try:
                flat_application = LazyFlatApplication.objects.filter(flat_application_id=request.data["flat_application_id"]).select_related('renter_id', 'landlord_id').get()
            except LazyFlatApplication.DoesNotExist:
                return JsonResponse("The flat application does not exist.", status=status.HTTP_404_NOT_FOUND, safe=False)
            flat_application.delete()
            return JsonResponse("Flat application deleted successfully.", status=status.HTTP_204_NO_CONTENT, safe=False)
        else:
            return JsonResponse('Flat Application ID not provided.', status=status.HTTP_400_BAD_REQUEST, safe=False)
        
    
    class LazyFlatApplicationDashboardAPIView(APIView):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        serializer_class = LazyFlatApplicationDashboardSerializer
        queryset = LazyFlatApplication.objects.all()

        @swagger_auto_schema(operation_description="Retrieve flat application dashboard",
                            request_body=LazyFlatApplicationDashboardSerializer)
        def get(self, request):
            """Retrieve flat application dashboard for user"""
            lazy_user = LazyUser.objects.get(username=request.user)
            lazy_user_profile = LazyUserProfile.objects.get(user=lazy_user)
            try:
                lazy_renter = LazyRenter.objects.get(profile_id=lazy_user_profile)
                flat_applications = LazyFlatApplication.objects.filter(renter_id=lazy_renter).select_related('landlord_id')
                serializer = LazyFlatApplicationDashboardSerializer(flat_applications, many=True)
                return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
            except LazyRenter.DoesNotExist:
                return JsonResponse("No flat applications found for the user.", status=status.HTTP_404_NOT_FOUND, safe=False)
            
        @swagger_auto_schema(operation_description="Update flat application",
                            request_body=LazyFlatApplicationDashboardSerializer)
        def put(self, request):
            """Update flat application"""
            if "flat_application_id" in request.data:
                try:
                    flat_application = LazyFlatApplication.objects.get(flat_application_id=request.data["flat_application_id"]).select_related('renter_id', 'landlord_id')
                except LazyFlatApplication.DoesNotExist:
                    return JsonResponse("The flat application does not exist.", status=status.HTTP_404_NOT_FOUND, safe=False)
                serializer = LazyFlatApplicationDashboardSerializer(flat_application, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, status=status.HTTP_200_OK)
                else:
                    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)
            else:
                return JsonResponse('Flat Application ID not provided.', status=status.HTTP_400_BAD_REQUEST, safe=False)

        
