"""Trainings 序列化器"""
from rest_framework import serializers
from .models import TrainingNotice, TrainingSignUp, TrainingNote


class TrainingNoticeSerializer(serializers.ModelSerializer):
    """训练通知序列化器"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    signup_count = serializers.SerializerMethodField()

    class Meta:
        model = TrainingNotice
        fields = [
            'id', 'title', 'content', 'location', 'train_date',
            'start_time', 'end_time', 'coach', 'max_participants',
            'signup_deadline', 'notice_type', 'status',
            'created_by', 'created_by_name', 'signup_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_signup_count(self, obj):
        return obj.signups.filter(status='registered').count()


class TrainingNoticeCreateSerializer(serializers.ModelSerializer):
    """创建训练通知序列化器"""
    class Meta:
        model = TrainingNotice
        fields = [
            'title', 'content', 'location', 'train_date',
            'start_time', 'end_time', 'coach', 'max_participants',
            'signup_deadline', 'notice_type'
        ]


class TrainingSignUpSerializer(serializers.ModelSerializer):
    """训练报名序列化器"""
    member_name = serializers.CharField(source='member.full_name', read_only=True)
    notice_title = serializers.CharField(source='notice.title', read_only=True)

    class Meta:
        model = TrainingSignUp
        fields = [
            'id', 'notice', 'notice_title', 'member', 'member_name',
            'signup_time', 'status'
        ]
        read_only_fields = ['id', 'signup_time']


class TrainingNoteSerializer(serializers.ModelSerializer):
    """训练笔记序列化器"""
    member_name = serializers.CharField(source='member.full_name', read_only=True)

    class Meta:
        model = TrainingNote
        fields = [
            'id', 'member', 'member_name', 'notice', 'title', 'content',
            'visibility', 'like_count', 'comment_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'like_count', 'comment_count', 'created_at', 'updated_at']


class TrainingNoteCreateSerializer(serializers.ModelSerializer):
    """创建训练笔记序列化器"""
    class Meta:
        model = TrainingNote
        fields = ['notice', 'title', 'content', 'visibility']
