from rest_framework import serializers
from .models import Network


class NetworkSerializer(serializers.ModelSerializer):
    # Включите связанный контакт и поставщика, если нужно
    contact = serializers.StringRelatedField()
    supplier = serializers.StringRelatedField()

    class Meta:
        model = Network
        fields = '__all__'
        read_only_fields = ('debt',)  # Запретить обновлять задолженность через API
