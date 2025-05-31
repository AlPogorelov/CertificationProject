from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, Contact, Network

User = get_user_model()


class BaseAPITestCase(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            email='testuser@mail.ru',
            password='testpass123',
            is_active=True
        )
        # Получаем JWT токен
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Тестовые данные
        self.product = Product.objects.create(
            name='Телевизор',
            model='SmartTV-2023',
            release_date='2023-01-01'
        )
        self.contact = Contact.objects.create(
            email='test@example.com',
            country='Russia',
            city='Moscow',
            street='Lenina',
            house_number='1'
        )
        self.network = Network.objects.create(
            name='Тестовый завод',
            level=0,
            contact=self.contact
        )
        self.network.products.add(self.product)


class ProductAPITests(BaseAPITestCase):
    def test_create_product(self):
        url = reverse('networks:products-list')
        data = {
            'name': 'Смартфон',
            'model': 'Galaxy S23',
            'release_date': '2023-02-01'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_product_unique_constraint(self):
        url = reverse('networks:products-list')
        data = {
            'name': 'Телевизор',  # Уже существует
            'model': 'SmartTV-2023',
            'release_date': '2023-01-01'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_products(self):
        url = reverse('networks:products-list') + '?name=Телевизор'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['model'], 'SmartTV-2023')


class ContactAPITests(BaseAPITestCase):
    def test_contact_creation(self):
        url = reverse('networks:contacts-list')
        data = {
            'email': 'new@example.com',
            'country': 'USA',
            'city': 'New York',
            'street': 'Broadway',
            'house_number': '100'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 2)
        self.assertEqual(response.data['city'], 'New York')

    def test_contact_filter(self):
        url = reverse('networks:contacts-list') + '?country=Russia'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class NetworkAPITests(BaseAPITestCase):
    def test_network_creation(self):
        url = reverse('networks:networks-list')
        data = {
            'name': 'Новый завод',
            'contact': self.contact.id,
            'products': [self.product.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['level'], 0)  # Проверка автоустановки уровня

    def test_debt_read_only(self):
        url = reverse('networks:networks-detail', args=[self.network.id])
        data = {'debt': 1000}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что debt не изменился
        updated_network = Network.objects.get(id=self.network.id)
        self.assertEqual(updated_network.debt, 0)
        self.assertEqual(response.data['debt'], '0.00')

    def test_supplier_hierarchy(self):
        # Убедимся, что начальная сеть - это завод (level=0)
        self.assertEqual(self.network.level, Network.FACTORY)

        # Создаем розничную сеть с поставщиком
        url = reverse('networks:networks-list')
        data = {
            'name': 'Розничная сеть',
            'supplier': self.network.id,
            'contact': self.contact.id,
            'products': [self.product.id]
        }
        response = self.client.post(url, data, format='json')

        # Проверяем успешное создание
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Получаем созданную сеть из базы
        new_network = Network.objects.get(id=response.data['id'])

        # Проверяем уровень (должен быть RETAIL=1)
        self.assertEqual(new_network.level, Network.RETAIL)

        # Проверяем связь с поставщиком
        self.assertEqual(new_network.supplier, self.network)

        # Дополнительная проверка через API
        detail_url = reverse('networks:networks-detail', args=[new_network.id])
        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.data['level'], Network.RETAIL)


class PermissionTests(APITestCase):
    def test_inactive_user_access(self):
        # Создаем неактивного пользователя
        user = User.objects.create_user(
            email='testusernotactive@mail.ru',
            password='testpass',
            is_active=False
        )
        url = reverse('users:token_obtain_pair')
        data = {
            'email': 'testusernotactive@mail.ru',
            'password': 'testpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)