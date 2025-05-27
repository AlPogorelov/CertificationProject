from rest_framework import serializers
from .models import Network, Product, Contact


class NetworkSerializer(serializers.ModelSerializer):
    contact = serializers.StringRelatedField()
    supplier = serializers.StringRelatedField()

    class Meta:
        model = Network
        fields = '__all__'
        read_only_fields = ('debt',)  # Запретить обновлять задолженность через API


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
