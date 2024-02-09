from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from .models import LazyUser
from .serializers import CreateUserSerializer, UpdateUserSerializer



class CreateUserAPI(CreateAPIView):
    queryset = LazyUser.objects.all()
    serializer_class = CreateUserSerializer


class UpdateUserAPI(UpdateAPIView):
    queryset = LazyUser.objects.all()
    serializer_class = UpdateUserSerializer

# class UserListView(generics.ListAPIView):
#     queryset = LazyUser.objects.all()
#     serializer_class = LazyUser
