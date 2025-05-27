from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Network
from .permissions import IsActiveUser
from .serializers import NetworkSerializer


class NetworkViewSet(viewsets.ModelViewSet):
    """ ViewSet для модели Network(сеть поставщиков)"""
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact__country']
