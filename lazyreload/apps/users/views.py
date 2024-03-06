from django.shortcuts import render, redirect, reverse
from rest_framework import generics, status
from rest_framework.views import APIView, View
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework import parsers
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer
from .forms import RegistrationForm
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from apps.core.utils import CVTextExtractor
from dotenv import load_dotenv
import os


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from .models import LazyUser, LazyUserProfile
from .serializers import LazyUserSerializer, LazyLoginSerializer, LazyUpdateUserSerializer , LazyUserProfileSerializer  # UpdateUserSerializer


@method_decorator(csrf_exempt, name='dispatch')
class CreateUserAPI(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'core/register.html')


    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.data)

        if form.is_valid():
            user = form.save()
            login(request, user)

            if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                serializer = LazyUserSerializer(user)
                return JsonResponse(serializer.data, status=201)
            else:
                return HttpResponseRedirect(reverse('users:userprofile', kwargs={'user_id': user.pk}))

        # Form is not valid
        errors = form.errors
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
           
            return JsonResponse({'errors': errors}, status=400)
        else:
            return render(request, 'core/register.html', {'errors': errors})
        
    

    #Creates a new user and generates an authentication token.
    @swagger_auto_schema(operation_description="Create a new user", request_body=LazyUserSerializer)

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)


class LoginView(APIView):
    permission_classes = [AllowAny]


    def get(self, request, *args, **kwargs):
        return render(request, 'core/login.html')  

    # Authenticates a user based on provided credentials and returns a token and user information.
    @swagger_auto_schema(operation_description="Login to application", request_body=LazyLoginSerializer)
    def post(self, request, *args, **kwargs):
        serializer = LazyLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username') 
        password = serializer.validated_data.get('password')
        user = None
        
        # if validation is true, extract username and password from validated data
        if username:
            user = authenticate(request, username=username, password=password)


        #if the user is valid, the user is logged and the token is created or retrieved

        if user:
            login(request, user)  
            token, created = Token.objects.get_or_create(user=user)
            user_serializer = LazyUserSerializer(user)
            response_data = {
                'token': token.key,
                'user': user_serializer.data
            }



            if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return Response({'detail': 'Successfuly logged in'}, status=status.HTTP_200_OK)
            else:
                return render(request, 'core/userprofile.html', {'username': user.username})

        else:
            if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return render(request, 'core/userprofile.html', {'error': 'Invalid credentials'})
                

class LazyUpdateUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # Updates a user's information
    @swagger_auto_schema(operation_description="Update a user's information", request_body=LazyUpdateUserSerializer)
    def put(self, request, user_id):
        try:
            user = LazyUser.objects.get(user_id=user_id)
            # Check authentication and permissions
            if not request.user.is_staff and request.user != user:
                return Response({'detail': 'You are not authorized to update this user.'}, status=status.HTTP_403_FORBIDDEN)

            serializer = LazyUpdateUserSerializer(user, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except LazyUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    

class LazyDeleteUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # Deletes a user with the specified ID
    @swagger_auto_schema(operation_description="Delete a user")
    def delete(self, request, user_id):
        try:
            user = LazyUser.objects.get(user_id=user_id)

            # Check authentication and permissions
            if not request.user.is_staff and request.user != user:
                return Response({'detail': 'You are not authorized to delete this user.'}, status=status.HTTP_403_FORBIDDEN)

            user.delete()
            return Response({'detail': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except LazyUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        

class UserListView(ListAPIView):
    queryset = LazyUser.objects.all()
    serializer_class = LazyUserSerializer
    permission_classes = [IsAdminUser] #need to be active for permission access control test, otherwise the test fails (403 expected but 200 gets returned resulting in F)
    

class LazyUserProfileView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LazyUserProfileSerializer
    parser_classes = [MultiPartParser, FormParser] #parsers handle different media types in the request
    renderer_classes = [JSONRenderer]
    
    @swagger_auto_schema(operation_description="Retrieve a user's profile", request_body=LazyUserProfileSerializer)
    def get_object(self):
        user_profile, created = LazyUserProfile.objects.get_or_create(user=self.request.user)
        return user_profile


    def get(self, request, *args, **kwargs):
        return render(request, 'core/userprofile.html')


    
    @swagger_auto_schema(operation_description="Update a user's profile", request_body=LazyUserProfileSerializer)
    def post(self, request, *args, **kwargs):
        # If a user profile already exists, update it, otherwise create a new one
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Extract the 'cv_file'
        cv_file = request.data.get('cv_file')
        
        # Check if a file is provided and then extracts the text from the file
        if cv_file:
            cv_text_generator = CVTextExtractor(
                OPENAI_API_KEY,
                file_path=cv_file,
            )
            cv_text = cv_text_generator.extract_cv_info()
            
        else:
            # If no file is provided, set cv_text to None
            cv_text = None

        # Update the user profile fields with the validated data
        user_profile = self.get_object()
        user_profile.use_case = serializer.validated_data.get('use_case')
        user_profile.cv_file = serializer.validated_data.get('cv_file')  
        user_profile.email = serializer.validated_data.get('email')
        user_profile.cv_text = cv_text
        user_profile.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HomeView(View):
    def get(self, request):
        return render (request, 'core/home.html')
    

class AboutUsView(View):
    def get(self, request):
        return render (request, 'core/aboutus.html')
    
class ContactView(View):
    def get(self, request):
        return render (request, 'core/contact.html')



    
