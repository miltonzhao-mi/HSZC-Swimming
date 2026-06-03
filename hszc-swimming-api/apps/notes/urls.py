"""Notes URL配置"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet, NoteCommentViewSet, NoteLikeViewSet

router = DefaultRouter()
router.register(r'', NoteViewSet, basename='notes')
router.register(r'comments', NoteCommentViewSet, basename='comments')
router.register(r'likes', NoteLikeViewSet, basename='likes')

urlpatterns = [
    path('', include(router.urls)),
]
