from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
#from drf_yasg.utils import swagger_auto_schema
from .models import LazyUser, LazyUserProfile
from .serializers import LazyUserSerializer, LazyLoginSerializer, LazyUpdateUserSerializer , LazyUserProfileSerializer  # UpdateUserSerializer




class CreateUserAPI(CreateAPIView):
    queryset = LazyUser.objects.all()
    serializer_class = LazyUserSerializer

    #Creates a new user and generates an authentication token.
    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)


class LoginView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        return render(request, 'users/login.html')  

    # Authenticates a user based on provided credentials and returns a token and user information.
    def post(self, request, *args, **kwargs):
        serializer = LazyLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username') 
        password = serializer.validated_data.get('password')
        user = None
        
        #if validation is true, extract username and password from validated data
        if username:
            user = authenticate(request, username=username, password=password)

        #if the user object is valid, the user is logged and the token is created or retrieved
        if user:
            login(request, user)  # Log the user in
            token, created = Token.objects.get_or_create(user=user)
            user_serializer = LazyUserSerializer(user)
            response_data = {
                'token': token.key,
                'user': user_serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
      

class LazyUpdateUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # Updates a user's information
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


class LazyUserProfileView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LazyUserProfileSerializer

    def get_object(self):
        user_profile, created = LazyUserProfile.objects.get_or_create(user=self.request.user)
        return user_profile

    # def put(self, request, *args, **kwargs):
    #     if not request.user == self.get_object().user:
    #         return self.permission_denied(request)

    #     return self.update(request, *args, **kwargs)



@api_view(["GET", "POST"])
def user_list_view(request):
    if request.method == "GET":
        queryset = LazyUser.objects.all()
        serializer = LazyUserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = LazyUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Token.objects.create(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
