"""Messages 视图"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Message, MessageRead
from .serializers import (
    MessageSerializer, MessageCreateSerializer, MessageReadSerializer
)
from apps.core.response import ApiResponse


class MessageViewSet(viewsets.ModelViewSet):
    """消息视图集"""
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_fields = ['message_type', 'is_published']
    search_fields = ['title', 'content']
    ordering_fields = ['-created_at', '-published_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer

    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user)
        if message.is_published:
            message.published_at = timezone.now()
            message.save()

    def perform_update(self, serializer):
        message = serializer.save()
        if message.is_published and not message.published_at:
            message.published_at = timezone.now()
            message.save()

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """获取未读消息数量"""
        count = MessageRead.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        return ApiResponse.success({'count': count})

    @action(detail=True, methods=['post'])
    def read(self, request, pk=None):
        """标记已读"""
        message = self.get_object()
        record, _ = MessageRead.objects.get_or_create(
            message=message,
            user=request.user,
            defaults={'is_read': True, 'read_at': timezone.now()}
        )
        if not record.is_read:
            record.is_read = True
            record.read_at = timezone.now()
            record.save()
        return ApiResponse.success(message='已标记已读')


class MessageReadViewSet(viewsets.ReadOnlyModelViewSet):
    """消息阅读记录视图集"""
    queryset = MessageRead.objects.all()
    serializer_class = MessageReadSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['is_read']

    @action(detail=False, methods=['get'])
    def my(self, request):
        """获取我的消息"""
        reads = MessageRead.objects.filter(user=request.user).order_by('-read_at')
        page = self.paginate_queryset(reads)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(reads, many=True)
        return ApiResponse.success(serializer.data)
