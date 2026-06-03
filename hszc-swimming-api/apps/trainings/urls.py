"""Trainings URL配置"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrainingNoticeViewSet, TrainingSignUpViewSet, TrainingNoteViewSet

router = DefaultRouter()
router.register(r'notices', TrainingNoticeViewSet, basename='notices')
router.register(r'signups', TrainingSignUpViewSet, basename='trainingsignups')
router.register(r'notes', TrainingNoteViewSet, basename='notes')

urlpatterns = [
    path('', include(router.urls)),
]
