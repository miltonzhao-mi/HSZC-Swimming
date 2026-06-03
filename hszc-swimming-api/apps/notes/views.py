"""Notes 视图"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.utils import timezone
from .models import Note, NoteComment, NoteLike
from .serializers import (
    NoteSerializer, NoteCreateSerializer,
    NoteCommentSerializer, NoteCommentCreateSerializer,
    NoteLikeSerializer
)
from apps.core.response import ApiResponse


class NoteViewSet(viewsets.ModelViewSet):
    """笔记视图集"""
    queryset = Note.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_fields = ['visibility', 'member']
    search_fields = ['title', 'content']
    ordering_fields = ['-created_at', '-like_count', '-comment_count']

    def get_serializer_class(self):
        if self.action == 'create':
            return NoteCreateSerializer
        return NoteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # 普通会员只能看公开笔记和自己
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(visibility='public') | Q(member=self.request.user.member_profile)
            )
        return queryset

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

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """点赞"""
        note = self.get_object()
        like, created = NoteLike.objects.get_or_create(
            note=note,
            member=request.user.member_profile
        )

        if created:
            note.like_count += 1
            note.save()

            # 记录活跃度
            from apps.members.models import MemberActivity
            MemberActivity.objects.create(
                member=request.user.member_profile,
                activity_type='note_like',
                activity_date=timezone.now().date(),
                description=f'点赞了笔记: {note.title}'
            )

            return ApiResponse.success(message='点赞成功')
        return ApiResponse.error('已点赞')

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """取消点赞"""
        note = self.get_object()
        deleted, _ = NoteLike.objects.filter(
            note=note,
            member=request.user.member_profile
        ).delete()

        if deleted:
            note.like_count = max(0, note.like_count - 1)
            note.save()
            return ApiResponse.success(message='取消成功')
        return ApiResponse.error('未点赞')


class NoteCommentViewSet(viewsets.ModelViewSet):
    """评论视图集"""
    queryset = NoteComment.objects.filter(is_deleted=False)
    serializer_class = NoteCommentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['note', 'parent']

    def get_serializer_class(self):
        if self.action == 'create':
            return NoteCommentCreateSerializer
        return NoteCommentSerializer

    def perform_create(self, serializer):
        comment = serializer.save(member=self.request.user.member_profile)

        # 更新笔记评论数
        note = comment.note
        note.comment_count += 1
        note.save()

        # 记录活跃度
        from apps.members.models import MemberActivity
        MemberActivity.objects.create(
            member=self.request.user.member_profile,
            activity_type='note_comment',
            activity_date=timezone.now().date(),
            description=f'评论了笔记: {note.title}'
        )

    @action(detail=True, methods=['delete'])
    def soft_delete(self, request, pk=None):
        """软删除评论"""
        comment = self.get_object()
        comment.is_deleted = True
        comment.save()

        # 更新笔记评论数
        note = comment.note
        note.comment_count = max(0, note.comment_count - 1)
        note.save()

        return ApiResponse.success(message='删除成功')


class NoteLikeViewSet(viewsets.ReadOnlyModelViewSet):
    """笔记点赞视图集"""
    queryset = NoteLike.objects.all()
    serializer_class = NoteLikeSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['note', 'member']
