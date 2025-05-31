from rest_framework import serializers
from .models import Network, Product, Contact


# class NetworkSerializer(serializers.ModelSerializer):
#     contact = serializers.StringRelatedField()
#     supplier = serializers.StringRelatedField()
#
#     class Meta:
#         model = Network
#         fields = '__all__'
#         read_only_fields = ('debt', 'level')  # Добавляем level в read-only
#
#     def create(self, validated_data):
#         # Извлекаем products отдельно, так как это ManyToMany поле
#         products_data = validated_data.pop('products', [])
#
#         # Создаем объект Network
#         network = Network.objects.create(**validated_data)
#
#         # Устанавливаем продукты
#         network.products.set(products_data)
#
#         # Обновляем уровень на основе supplier
#         if network.supplier:
#             network.level = network.supplier.level + 1
#             if network.level > Network.ENTREPRENEUR:
#                 network.level = Network.ENTREPRENEUR
#             network.save()
#
#         return network
#
#     def validate(self, data):
#         supplier = data.get('supplier')
#         if supplier and supplier.level == Network.ENTREPRENEUR:
#             raise serializers.ValidationError(
#                 "Индивидуальный предприниматель не может быть поставщиком"
#             )
#         return data
class NetworkSerializer(serializers.ModelSerializer):
    contact = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all())
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Network.objects.all(),
        required=False,
        allow_null=True
    )
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all()
    )

    class Meta:
        model = Network
        fields = '__all__'
        read_only_fields = ('debt', 'created_at')

    def create(self, validated_data):
        products = validated_data.pop('products')
        instance = Network.objects.create(**validated_data)
        instance.products.set(products)

        # Принудительно обновляем уровень после создания
        instance._update_level()
        instance.save()

        return instance

    def update(self, instance, validated_data):
        products = validated_data.pop('products', None)
        instance = super().update(instance, validated_data)

        if products is not None:
            instance.products.set(products)

        # Принудительно обновляем уровень после обновления
        instance._update_level()
        instance.save()

        return instance


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
