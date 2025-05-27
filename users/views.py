from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets, status

from users.models import User
from users.serializers import UserSerializer


class UsersViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
