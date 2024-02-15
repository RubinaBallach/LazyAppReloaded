from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import LazyUser, LazyUserProfile
from .serializers import LazyUserSerializer, LazyUserProfileSerializer  # UpdateUserSerializer



class CreateUserAPI(CreateAPIView):
    queryset = LazyUser.objects.all()
    serializer_class = LazyUserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)


class UpdateUserAPI(UpdateAPIView):
    queryset = LazyUser.objects.all()
    serializer_class = LazyUserSerializer

class UserListView(ListAPIView):
    queryset = LazyUser.objects.all()
    serializer_class = LazyUserSerializer



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
