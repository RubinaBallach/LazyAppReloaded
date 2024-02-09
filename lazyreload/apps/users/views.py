from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from .models import LazyUser
from .serializers import LazyUserSerializer  #UpdateUserSerializer



class CreateUserAPI(CreateAPIView):
    queryset = LazyUser.objects.all()
    serializer_class = LazyUserSerializer


class UpdateUserAPI(UpdateAPIView):
    queryset = LazyUser.objects.all()
    serializer_class = LazyUserSerializer

# class UserListView(generics.ListAPIView):
#     queryset = LazyUser.objects.all()
#     serializer_class = LazyUser
