"""Users URL配置"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, UserViewSet, RoleViewSet, OperationLogViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'', UserViewSet, basename='users')
router.register(r'roles', RoleViewSet, basename='roles')
router.register(r'logs', OperationLogViewSet, basename='logs')

urlpatterns = [
    path('', include(router.urls)),
]
