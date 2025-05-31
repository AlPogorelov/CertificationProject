from django.urls import path
from .views import UsersViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .apps import UsersConfig
from rest_framework.routers import DefaultRouter

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), )
    ] + router.urls
