from rest_framework.routers import DefaultRouter

from .apps import NetworkConfig
from .views import NetworkViewSet

app_name = NetworkConfig.name

router = DefaultRouter()
router.register(r'networks', NetworkViewSet)

urlpatterns = [
]

urlpatterns += router.urls
