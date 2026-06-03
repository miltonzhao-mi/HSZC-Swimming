"""Messages URL配置"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, MessageReadViewSet

router = DefaultRouter()
router.register(r'', MessageViewSet, basename='messages')
router.register(r'reads', MessageReadViewSet, basename='messagereads')

urlpatterns = [
    path('', include(router.urls)),
]
