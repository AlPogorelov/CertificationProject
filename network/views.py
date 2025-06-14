from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Network, Product, Contact
from .permissions import IsActiveUser
from .serializers import NetworkSerializer, ProductSerializer, ContactSerializer


class NetworkViewSet(viewsets.ModelViewSet):
    """ ViewSet для модели Network(сеть поставщиков)"""
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact__country']


class ProductViewSet(viewsets.ModelViewSet):
    """ ViewSet для модели Product(продукт поставщиков)"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'model']


class ContactViewSet(viewsets.ModelViewSet):
    """ ViewSet для модели Product(продукт поставщиков)"""
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email', 'country', 'city']
