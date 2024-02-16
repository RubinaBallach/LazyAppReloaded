from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from .models import LazyUser, LazyUserProfile
from .serializers import LazyUserSerializer, LazyLoginSerializer, LazyUpdateUserSerializer , LazyUserProfileSerializer  # UpdateUserSerializer




class CreateUserAPI(CreateAPIView):
    queryset = LazyUser.objects.all()
    serializer_class = LazyUserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return render(request, 'users/login.html')  # Create a login.html template

    def post(self, request, *args, **kwargs):
        serializer = LazyLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        #email = serializer.validated_data.get('email')  
        password = serializer.validated_data.get('password')
        user = None
        if username:
            user = authenticate(request, username=username, password=password)
        # elif email:
        #     user = authenticate(request, email=email, password=password)

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

    def put(self, request, user_id):
        try:
            user = LazyUser.objects.get(id=user_id)
        except LazyUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = LazyUpdateUserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserListView(ListAPIView):
    queryset = LazyUser.objects.all()
    serializer_class = LazyUserSerializer


class LazyUserProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LazyUserProfile.objects.all()
    serializer_class = LazyUserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return LazyUserProfile.objects.get(user=self.request.user)



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
