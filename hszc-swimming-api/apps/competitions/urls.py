"""Competitions URL配置"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompetitionViewSet, SignUpViewSet, ScoreViewSet,
    ScoreFileViewSet, EventItemViewSet
)

router = DefaultRouter()
router.register(r'', CompetitionViewSet, basename='competitions')
router.register(r'signups', SignUpViewSet, basename='signups')
router.register(r'scores', ScoreViewSet, basename='scores')
router.register(r'files', ScoreFileViewSet, basename='scorefiles')
router.register(r'items', EventItemViewSet, basename='eventitems')

urlpatterns = [
    path('', include(router.urls)),
]
