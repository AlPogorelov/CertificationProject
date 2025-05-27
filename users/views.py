from rest_framework import viewsets
from users.models import User
from users.serializers import UserSerializer


class UsersViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
