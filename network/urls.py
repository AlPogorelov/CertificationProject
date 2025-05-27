from rest_framework.routers import DefaultRouter

from .apps import NetworkConfig
from .views import NetworkViewSet, ProductViewSet, ContactViewSet

app_name = NetworkConfig.name

router = DefaultRouter()
router.register(r'networks', NetworkViewSet, basename='networks')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'contacts', ContactViewSet, basename='contacts')

urlpatterns = [
]

urlpatterns += router.urls
