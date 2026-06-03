"""Trainings 视图"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import TrainingNotice, TrainingSignUp, TrainingNote
from .serializers import (
    TrainingNoticeSerializer, TrainingNoticeCreateSerializer,
    TrainingSignUpSerializer,
    TrainingNoteSerializer, TrainingNoteCreateSerializer
)
from apps.core.response import ApiResponse


class TrainingNoticeViewSet(viewsets.ModelViewSet):
    """训练通知视图集"""
    queryset = TrainingNotice.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'notice_type']
    search_fields = ['title', 'content', 'coach']
    ordering_fields = ['-train_date', '-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return TrainingNoticeCreateSerializer
        return TrainingNoticeSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def sign_up(self, request, pk=None):
        """报名训练"""
        notice = self.get_object()

        if timezone.now() > notice.signup_deadline:
            return ApiResponse.error('报名已截止')

        member_id = request.data.get('member_id')
        if not member_id:
            return ApiResponse.error('缺少member_id')

        signup, created = TrainingSignUp.objects.get_or_create(
            notice=notice,
            member_id=member_id,
            defaults={'status': 'registered'}
        )

        if not created:
            return ApiResponse.error('已报名')

        # 记录活跃度
        from apps.members.models import MemberActivity
        MemberActivity.objects.create(
            member_id=member_id,
            activity_type='training_signup',
            activity_date=timezone.now().date(),
            description=f'报名参加训练: {notice.title}'
        )

        return ApiResponse.created(TrainingSignUpSerializer(signup).data, '报名成功')

    @action(detail=True, methods=['get'])
    def signups(self, request, pk=None):
        """获取报名列表"""
        notice = self.get_object()
        signups = notice.signups.filter(status='registered')
        serializer = TrainingSignUpSerializer(signups, many=True)
        return ApiResponse.success(serializer.data)


class TrainingSignUpViewSet(viewsets.ModelViewSet):
    """训练报名视图集"""
    queryset = TrainingSignUp.objects.all()
    serializer_class = TrainingSignUpSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['notice', 'status']

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消报名"""
        signup = self.get_object()
        signup.status = 'cancelled'
        signup.save()
        return ApiResponse.success(message='取消成功')


class TrainingNoteViewSet(viewsets.ModelViewSet):
    """训练笔记视图集"""
    queryset = TrainingNote.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_fields = ['visibility', 'member']
    search_fields = ['title', 'content']
    ordering_fields = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return TrainingNoteCreateSerializer
        return TrainingNoteSerializer

    def perform_create(self, serializer):
        serializer.save(member=self.request.user.member_profile)

        # 记录活跃度
        from apps.members.models import MemberActivity
        MemberActivity.objects.create(
            member=self.request.user.member_profile,
            activity_type='note_publish',
            activity_date=timezone.now().date(),
            description=f'发布训练心得: {serializer.validated_data.get("title")}'
        )

    @action(detail=False, methods=['get'])
    def public(self, request):
        """获取公开笔记"""
        notes = TrainingNote.objects.filter(visibility='public').order_by('-created_at')
        page = self.paginate_queryset(notes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(notes, many=True)
        return ApiResponse.success(serializer.data)
