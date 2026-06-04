"""Profiles URL配置"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemberProfileViewSet, PerformanceRecordViewSet

router = DefaultRouter()
router.register(r'member', MemberProfileViewSet, basename='profiles')
router.register(r'records', PerformanceRecordViewSet, basename='performance-records')

urlpatterns = [
    path('', include(router.urls)),
]