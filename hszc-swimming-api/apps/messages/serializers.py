"""Messages 序列化器"""
from rest_framework import serializers
from .models import Message, MessageRead


class MessageSerializer(serializers.ModelSerializer):
    """消息序列化器"""
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    message_type_display = serializers.CharField(source='get_message_type_display', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'title', 'content', 'message_type', 'message_type_display',
            'sender', 'sender_name', 'is_published', 'published_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MessageCreateSerializer(serializers.ModelSerializer):
    """创建消息序列化器"""
    class Meta:
        model = Message
        fields = ['title', 'content', 'message_type', 'is_published']


class MessageReadSerializer(serializers.ModelSerializer):
    """消息阅读记录序列化器"""
    message_title = serializers.CharField(source='message.title', read_only=True)

    class Meta